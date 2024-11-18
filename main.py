from flask import (
    Flask,
    url_for,
    request,
    render_template,
    send_from_directory,
    jsonify,
    send_file,
    session,
    redirect,
)
from model import Booking, Flight
from waitress import serve
from helper import (
    parse_description,
    parse_departure,
    parse_arrival,
    check_flight_pattern,
    extract_flight_info,
    abbreviated_place_name,
    abbreviate_airport_name,
    md5_hash,
)
import re
import os
from weasyprint import HTML
from datetime import datetime
import threading
from flask import Response
import hashlib
from db import db, Register
from datetime import timedelta
import pytz
from pdf_manager import PDFManager
import zipfile
import tempfile
from flask import after_this_request
from collections import defaultdict
import base64

app = Flask(__name__)
app.secret_key = os.urandom(24)
db_path = "dblfihgt.db"
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.abspath(db_path)}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static\\uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db.init_app(app)

# global_booking = None
logo_path = "vietnam-airline-logo.png"

user_requests = defaultdict(int) 
MAX_REQUESTS_PER_DAY = 5 
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

if not os.path.exists(db_path):
    print("Database not found. Creating new database.")
    with app.app_context():
        db.create_all()
else:
    print("Database already exists.")

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/parsepage", methods=["GET"])
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

@app.route("/")
def home():
    user_id = session.get("user_id")  
    usertype = session.get("usertype")  
    booking = Booking(None, None, [], None, [], Flight(), Flight())
    return render_template("parse_data.html", booking=booking, user_id=user_id, usertype=usertype)
@app.route("/login_page")
def login_page():
    return render_template("login.html")
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        print(request.form["password"])
        email = request.form["email"]
        password = md5_hash(request.form["password"])
        user = Register.query.filter_by(email=email, password=password).first()
        print(email)

        if user:
            session["user_id"] = user.id
            session["usertype"] = user.usertype
            session.permanent = True
            if user.usertype == "guest":
                session.permanent = True 
                app.permanent_session_lifetime = timedelta(hours=1) 
            elif user.usertype == "admin":
                session.permanent = True
                app.permanent_session_lifetime = timedelta(days=1)
            if user.usertype == "admin":
                return redirect(url_for("admin_overview"))
            elif user.usertype in ["guest"]:
                return redirect(url_for("parse_page"))
        else:
            return "Notok", 400
    return render_template("login.html")
@app.route("/account", methods=["GET"])
def admin_account():
    if "user_id" in session and session["usertype"] in ["admin", "guest"]:
        user = Register.query.filter_by(id=session["user_id"]).first()
        if user:
            return render_template("admin/account.html", user_name=user.user, user_type=user.usertype, email=user.email)
        else:
            return "Không tìm thấy thông tin người dùng"
    else:
        return redirect(url_for("login"))
@app.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return "OK", 200
@app.before_request
def limit_guest_session():
    if "user_id" in session and session["usertype"] == "guest":
        timezone = pytz.timezone('Asia/Ho_Chi_Minh')
        now = datetime.now(timezone)

        if 'last_activity' not in session:
            session['last_activity'] = now
        else:
            last_activity = session['last_activity'].astimezone(timezone)
            if (now - last_activity) > timedelta(hours=1):
                session.pop('user_id', None)
                session.pop('usertype', None)
                return redirect(url_for("login_page"))

        session['last_activity'] = now
@app.route("/numbertool", methods=["GET"])
def number_tool():
    if "user_id" in session and session["usertype"] in ["admin", "guest"]:
        user_id = session.get("user_id")  
        user = Register.query.filter_by(id=session["user_id"]).first()
        if user:
            return render_template("number.html", user_name=user.user, user_id=user_id)
        else:
            return "Không tìm thấy thông tin người dùng"
    else:
        return redirect(url_for("login"))    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
    # serve(app, host='0.0.0.0', port=5000)
