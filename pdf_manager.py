from weasyprint import HTML
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
import os
from model import Flight
from helper import abbreviated_place_name
import zipfile
from tempfile import TemporaryDirectory
import base64

class PDFManager:
    @staticmethod
    def get_image_base64(image_path):
        """Convert image to base64 string"""
        if not os.path.exists(image_path):
            return ''
        
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')
    @staticmethod
    def create_pdf_filename(passenger_name, booking):
        passenger_name_for_filename = passenger_name.replace(" ", "-").replace("/", "-")
        date_issue = booking.date_issue.replace(" ", "")
        formatted_date_issue = date_issue.upper()

        flight1_departure = abbreviated_place_name(booking.flight1.departure_place)
        flight1_arrival = abbreviated_place_name(booking.flight1.arrival_place)
        flight1_abbreviation = f"{flight1_departure}-{flight1_arrival}"

        flight2_abbreviation = ""

        if booking.flight2:
            flight2_departure = abbreviated_place_name(booking.flight2.departure_place)
            flight2_arrival = abbreviated_place_name(booking.flight2.arrival_place)

            if flight1_arrival == flight2_departure:
                flight2_abbreviation = f"-{flight2_arrival}"
            else:
                flight2_abbreviation = f"-{flight2_departure}-{flight2_arrival}"

        pdf_filename = f"{passenger_name_for_filename}_{formatted_date_issue}_{flight1_abbreviation}{flight2_abbreviation}.pdf"
        
        return pdf_filename

    @staticmethod
    def print_pdf(booking, passenger_name, logo_path, selected_fields=None, logo_user=None):

        PDFManager.update_flight_times(booking)
        pdf_filename = PDFManager.create_pdf_filename(passenger_name, booking)
        pdf_path = os.path.abspath(pdf_filename)

        logo_base64 = PDFManager.get_image_base64(logo_path)

        template_path = os.path.abspath("template_ticket.html")
        html_content = PDFManager.render_pdf_template(template_path, booking, logo_base64, selected_fields,logo_user=logo_user )

        HTML(string=html_content).write_pdf(pdf_path)

        return pdf_path

    @staticmethod
    def render_pdf_template(template_path, booking, logo_base64, selected_fields=None, logo_user=None ):
        env = Environment(loader=FileSystemLoader(os.path.dirname(template_path)))
        template = env.get_template(os.path.basename(template_path))
        return template.render(booking=booking, logo_base64= logo_base64, selected_fields=selected_fields, logo_user=logo_user)

    @staticmethod
    def update_flight_times(booking):
        correct_format = "%a, %d %b %Y, %H:%M"

        def is_time_correct_format(flight_time):
            try:
                datetime.strptime(flight_time, correct_format)
                return True
            except ValueError:
                return False

        year = datetime.strptime(booking.date_issue, "%d %B %Y").year

        if booking.flight1:
            if not is_time_correct_format(booking.flight1.departure_time):
                departure_datetime = datetime.strptime(
                    booking.flight1.departure_time, "%d %b %H:%M"
                )
                booking.flight1.departure_time = departure_datetime.replace(
                    year=year
                ).strftime(correct_format)

            if not is_time_correct_format(booking.flight1.arrival_time):
                arrival_datetime = datetime.strptime(
                    booking.flight1.arrival_time, "%d %b %H:%M"
                )
                booking.flight1.arrival_time = arrival_datetime.replace(year=year).strftime(
                    correct_format
                )

        if booking.flight2:
            if not is_time_correct_format(booking.flight2.departure_time):
                departure_datetime = datetime.strptime(
                    booking.flight2.departure_time, "%d %b %H:%M"
                )
                booking.flight2.departure_time = departure_datetime.replace(
                    year=year
                ).strftime(correct_format)

            if not is_time_correct_format(booking.flight2.arrival_time):
                arrival_datetime = datetime.strptime(
                    booking.flight2.arrival_time, "%d %b %H:%M"
                )
                booking.flight2.arrival_time = arrival_datetime.replace(year=year).strftime(
                    correct_format
                )
    @staticmethod
    def create_all_pdfs(booking, logo_path, selected_fields=None, logo_user=None ):
        print(logo_user)
        zip_dir = os.path.join(os.path.dirname(__file__), 'zip')        
        zip_filename = os.path.join(zip_dir, "all_tickets.zip")

        if os.path.exists(zip_filename):
            os.remove(zip_filename)

        PDFManager.update_flight_times(booking)
        pdf_files = []
        for passenger in booking.passenger_name:
            passenger_name = passenger
            pdf_path = PDFManager.print_pdf(booking, passenger_name, logo_path, selected_fields, logo_user)
            pdf_files.append(pdf_path)
        with zipfile.ZipFile(zip_filename, "w") as zipf:
            for pdf in pdf_files:
                zipf.write(pdf, os.path.basename(pdf))
        for pdf in pdf_files:
            os.remove(pdf)
        return zip_filename
