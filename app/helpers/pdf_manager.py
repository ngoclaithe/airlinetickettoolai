from weasyprint import HTML
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
import os
from ..models.flight import Flight
from .parse_data_helpers import abbreviated_place_name, abbreviate_airport_name
import zipfile
from tempfile import TemporaryDirectory
import base64
from flask import session

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
        passenger_name_for_filename = passenger_name.replace(" ", "_").replace("/", "_")
        flight1_departure_time = booking.flight1.departure_time.split(',')[1].strip()
        flight1_departure_time = flight1_departure_time.replace(" ", "")
        formatted_flight1_departure_time = flight1_departure_time.upper()

        flight1_departure_unmap = abbreviated_place_name(booking.flight1.departure_place)
        flight1_departure_mapped = abbreviate_airport_name(flight1_departure_unmap)
        flight1_arrival_unmap = abbreviated_place_name(booking.flight1.arrival_place)
        flight1_arrival_mapped = abbreviate_airport_name(flight1_arrival_unmap)
        flight1_abbreviation = f"{flight1_departure_mapped}{flight1_arrival_mapped}"
        flight2_abbreviation = ""

        if booking.flight2:
            flight2_departure_time = booking.flight2.departure_time.split(',')[1].strip()
            flight2_departure_time = flight2_departure_time.replace(" ", "")
            formatted_flight2_departure_time = flight2_departure_time.upper()
            flight2_departure_unmap = abbreviated_place_name(booking.flight2.departure_place)
            flight2_departure_mapped = abbreviate_airport_name(flight2_departure_unmap)
            flight2_arrival_unmap = abbreviated_place_name(booking.flight2.arrival_place)
            flight2_arrival_mapped = abbreviate_airport_name(flight2_arrival_unmap)
            # if flight1_arrival_mapped == flight2_departure_mapped:
            #     flight2_abbreviation = f"{flight2_arrival_mapped}"
            # else:
            flight2_abbreviation = f"{flight2_departure_mapped}{flight2_arrival_mapped}"

        pdf_filename = f"{passenger_name_for_filename}_{formatted_flight1_departure_time}_{flight1_abbreviation}_{formatted_flight2_departure_time}_{flight2_abbreviation}.pdf"
        
        return pdf_filename

    @staticmethod
    def print_pdf(booking, passenger_name, logo_path, selected_fields=None, logo_user=None):
        current_dir = os.path.dirname(__file__) 
        PDFManager.update_flight_times(booking)
        pdf_filename = PDFManager.create_pdf_filename(passenger_name, booking)
        pdf_path = os.path.abspath(pdf_filename)
        logo_dir = os.path.join(current_dir, '..')  
        logo_path_dir = os.path.join(logo_dir, logo_path)
        logo_base64 = PDFManager.get_image_base64(logo_path_dir)
        
        template_dir = os.path.join(current_dir, '..')  
        template_name = 'template_ticket.html'  
        template_path = os.path.join(template_dir, template_name)

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
    def create_all_pdfs(booking, logo_path, selected_fields=None, logo_user=None):
        user_id = session.get('user_id', 'default_user')  
        app_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))  
        zip_dir = os.path.join(app_root, 'app', 'static', 'zip') 
        if not os.path.exists(zip_dir):
            os.makedirs(zip_dir)
        
        # zip_filename = os.path.join(zip_dir, "all_tickets.zip")
        zip_filename = os.path.join(zip_dir, f"{user_id}_all_tickets.zip")
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