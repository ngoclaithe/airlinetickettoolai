from flask import Flask, request, render_template, send_from_directory, jsonify, send_file, Response
from model import Booking, Flight
from waitress import serve
from helper import (
    parse_description,
    parse_departure,
    parse_arrival,
    check_flight_pattern,
    extract_flight_info,
    abbreviated_place_name,
)
import re
import os
from pdf_manager import PDFManager  
from datetime import datetime

app = Flask(__name__, static_url_path="", static_folder="static")

global_booking = None

@app.route("/parsedata", methods=["POST"])
def parse_data():
    global global_booking

    try:
        form_data = request.form.get("data", "").replace("\r\n", "\n")
        data = f'"""{form_data}"""'

        booking_ref = re.search(r"BOOKING REF:\s*(\w+)", data)
        date_issue = re.search(r"DATE:\s*(\d{1,2}\s+\w+\s+\d{4})", data)

        reservation_status = "CONFIRMED"

        ticket_matches = re.findall(r"TICKET:\s*(.*?)\s*FOR\s*(.*?)\n", data)
        tickets = [ticket[0].strip() for ticket in ticket_matches] if ticket_matches else []
        passenger_names = [ticket[1].strip() for ticket in ticket_matches] if ticket_matches else []

        flight_data_pattern = re.compile(r"(FLIGHT\s+.+?)\n-+\n(.+?)(EQUIPMENT:\s*.+?)\n", re.DOTALL)
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
            baggage = flight_info.get("Baggage", "").strip() if "Baggage" in flight_info else None
            meal = flight_info.get("Meal", "").strip() if "Meal" in flight_info else None
            nonstop = flight_info.get("NonStop", "").strip() if "NonStop" in flight_info else None
            equipment = flight_info.get("Equipment", "").strip() if "Equipment" in flight_info else None

            des, des_time = parse_description(description)
            departure_place, departure_terminal, departure_time = parse_departure(departure)
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
                flight2
            )
            return render_template("index.html", booking=global_booking, missing_info=missing_info)

        return jsonify({"error": "Không có dữ liệu chuyến bay"}), 400

    except Exception as e:
        print(f"Lỗi: {e}")
        return jsonify({"error": "Lỗi xử lý dữ liệu"}), 500


@app.route("/download_pdf", methods=["POST"])
def download_pdf():
    global global_booking
    data = request.get_json()
    passenger_name = data.get("passenger_name")

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

    pdf_path = PDFManager.print_pdf(filtered_booking, passenger_name)
    with open(pdf_path, "rb") as f:
        pdf_data = f.read()
    response = Response(pdf_data, mimetype='application/pdf')
    response.headers.set('Content-Disposition', f'attachment; filename={os.path.basename(pdf_path)}')

    return response
@app.route("/")
def index():
    booking = Booking(None, None, [], None, [], Flight(), Flight())
    return render_template("index.html", booking=booking)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
    # serve(app, host='0.0.0.0', port=5000)