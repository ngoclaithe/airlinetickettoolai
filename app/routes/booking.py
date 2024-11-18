from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify, Response
from ..models.flight import Flight
from ..models.booking import Booking
from ..models.register import Register
from ..helpers.parse_data_helpers import (
    parse_description,
    parse_departure,
    parse_arrival,
    check_flight_pattern,
    extract_flight_info,
    abbreviated_place_name,
    abbreviate_airport_name,
    md5_hash,
)
from datetime import timedelta
import re
from ..helpers.pdf_manager import PDFManager
import os

bp = Blueprint('booking', __name__)

@bp.route('/parse', methods=['GET'])
def parse_page():
    if "user_id" in session and session["usertype"] in ["admin", "guest"]:
        user_id = session.get("user_id")  
        user = Register.query.filter_by(id=session["user_id"]).first()
        booking = Booking(None, None, [], None, [], Flight(), Flight())
        if user:
            return render_template("parse_data.html", user_name=user.user, booking=booking, user_id=user_id)
        else:
            return "Không tìm thấy thông tin người dùng"
    else:
        return redirect(url_for("login"))
@bp.route("/parsedata", methods=["POST"])
def parse_data():
    ip_address = request.remote_addr
    is_logged_in = "user_id" in session and session["usertype"] in ["admin", "guest"]
    if not is_logged_in:
        today = datetime.now().date()
        if user_requests[ip_address] >= MAX_REQUESTS_PER_DAY:
            return redirect(url_for("login_page"))
        user_requests[ip_address] += 1
    if request.method == "POST":
        global logo_path
        try:
            logo= request.form.get("logo_ticket")
            print(logo)
            if logo == "vna":
                logo_path = "vietnam-airline-logo.png"
            elif logo == "vietjet":
                logo_path = "vietjet-logo.png"
            elif logo == "bamboo":
                logo_path = "bamboo-logo.png"

            image = request.files.get("image")
            if image:
                if allowed_file(image.filename):
                    filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{image.filename}"
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    image.save(filepath)
                    session['uploaded_image_path'] = filepath
                    print("Session data on download_pdf:", session['uploaded_image_path'])
                else:
                    return jsonify({"error": "Ảnh tải lên không hợp lệ, chỉ chấp nhận các định dạng như .jpg, .png, .jpeg"}), 400
            else:
                session['uploaded_image_path'] = None
                filename = None


            form_data = request.form.get("data", "").replace("\r\n", "\n")
            data = f'"""{form_data}"""'

            booking_ref = re.search(r"BOOKING REF:\s*(\w+)", data)
            date_issue = re.search(r"DATE:\s*(\d{1,2}\s+\w+\s+\d{4})", data)

            reservation_status = "CONFIRMED"

            ticket_matches = re.findall(r"TICKET:\s*(.*?)\s*FOR\s*(.*?)\n", data)
            tickets = (
                [ticket[0].strip() for ticket in ticket_matches] if ticket_matches else []
            )
            passenger_names = (
                [ticket[1].strip() for ticket in ticket_matches] if ticket_matches else []
            )

            flight_data_pattern = re.compile(
                r"(FLIGHT\s+.+?)\n-+\n(.+?)(EQUIPMENT:\s*.+?)\n", re.DOTALL
            )
            flight_data_matches = re.findall(flight_data_pattern, data)

            data1 = flight_data_matches[0] if len(flight_data_matches) > 0 else None
            data2 = flight_data_matches[1] if len(flight_data_matches) > 1 else None

            def create_flight_object(flight_info):
                if not flight_info:
                    return None

                description = flight_info.get("Description", "").strip()
                departure = flight_info.get("Departure", "").strip()
                arrival = flight_info.get("Arrival", "").strip()
                economy_class = flight_info.get("Economy Class", "").strip()
                duration = flight_info.get("Duration", "").strip()
                baggage = (
                    flight_info.get("Baggage", "").strip()
                    if "Baggage" in flight_info
                    else None
                )
                meal = (
                    flight_info.get("Meal", "").strip() if "Meal" in flight_info else None
                )
                nonstop = (
                    flight_info.get("NonStop", "").strip()
                    if "NonStop" in flight_info
                    else None
                )
                equipment = (
                    flight_info.get("Equipment", "").strip()
                    if "Equipment" in flight_info
                    else None
                )

                des, des_time = parse_description(description)
                departure_place, departure_terminal, departure_time = parse_departure(
                    departure
                )
                arrival_place, arrival_terminal, arrival_time = parse_arrival(arrival)

                return Flight(
                    des,
                    departure,
                    arrival,
                    duration,
                    equipment,
                    baggage,
                    meal,
                    nonstop,
                    departure_place=departure_place,
                    departure_terminal=departure_terminal,
                    departure_time=departure_time,
                    arrival_place=arrival_place,
                    arrival_terminal=arrival_terminal,
                    arrival_time=arrival_time,
                    des_time=des_time,
                    economy_class=economy_class,
                )

            if data1 or data2:
                missing_info = None
                if data1 and data2:
                    missing_info = check_flight_pattern(data1, data2)
                    flight_info1 = extract_flight_info(data1)
                    flight_info2 = extract_flight_info(data2)
                    flight1 = create_flight_object(flight_info1)
                    flight2 = create_flight_object(flight_info2)
                elif data1 and not data2:
                    flight_info1 = extract_flight_info(data1)
                    flight1 = create_flight_object(flight_info1)
                    flight2 = None
                else:
                    flight1 = flight2 = None

                global_booking = Booking(
                    booking_ref.group(1) if booking_ref else None,
                    date_issue.group(1) if date_issue else None,
                    passenger_names,
                    reservation_status,
                    tickets,
                    flight1,
                    flight2,
                )
                session['booking'] = global_booking.to_dict()
                return jsonify({
                    "booking": global_booking.to_dict(),
                    "missing_info": missing_info,
                    "logo_path": logo_path,
                    "logo_user": filename
                }), 200

            return jsonify({"error": "Không có dữ liệu chuyến bay"}), 400

        except Exception as e:
            print(f"Lỗi: {e}")
            return jsonify({"error": "Lỗi xử lý dữ liệu"}), 500
@bp.route("/download_pdf", methods=["POST"])
def download_pdf():
    global logo_path

    booking_data = session.get('booking')
    data = request.get_json()
    passenger_name = data.get("passenger_name")
    selected_fields = data.get("selected_fields", [])

    global_booking = Booking.from_dict(booking_data)
    print("Selected fields:", selected_fields)

    if not passenger_name:
        return "Passenger name is required", 400

    try:
        passenger_index = global_booking.passenger_name.index(passenger_name)
    except ValueError:
        return jsonify({"error": "Không tìm thấy hành khách trong danh sách"}), 404

    filtered_booking = Booking(
        booking_ref=global_booking.booking_ref,
        date_issue=global_booking.date_issue,
        passenger_name=[global_booking.passenger_name[passenger_index]],
        reservation_status=global_booking.reservation_status,
        ticket=[global_booking.ticket[passenger_index]],
        flight1=global_booking.flight1,
        flight2=global_booking.flight2,
    )
    print("Session data on download_pdf:", session)
    logo_user_path = session.get('uploaded_image_path')
    print("Logo user path:",logo_user_path)
    logo_user_base64 = None

    if logo_user_path and os.path.exists(logo_user_path):
        with open(logo_user_path, "rb") as logo_file:
            logo_user_base64 = base64.b64encode(logo_file.read()).decode('utf-8')
    # print(logo_user_base64)
    pdf_path = PDFManager.print_pdf(filtered_booking, passenger_name, logo_path, selected_fields, logo_user_base64)
    with open(pdf_path, "rb") as f:
        pdf_data = f.read()
    response = Response(pdf_data, mimetype="application/pdf")
    response.headers.set(
        "Content-Disposition",
        f"attachment; filename={PDFManager.create_pdf_filename(passenger_name, filtered_booking)}",
    )

    try:
        print(pdf_path)
        os.remove(pdf_path)
    except Exception as e:
        print(f"Error removing file: {e}")

    return response
@bp.route("/download_all_pdf", methods=["POST"])
def download_all_pdf():
    global logo_path
    booking_data = session.get('booking')
    global_booking = Booking.from_dict(booking_data)
    data = request.get_json()
    selected_fields = data.get("selected_fields", [])
    logo_user = session.get('uploaded_image_base64')
    zip_path = PDFManager.create_all_pdfs(global_booking, logo_path, selected_fields, logo_user)
    print(zip_path)

    return send_file(
        zip_path,
        mimetype="application/zip",
        as_attachment=True,
        download_name='all_tickets.zip',
    )
