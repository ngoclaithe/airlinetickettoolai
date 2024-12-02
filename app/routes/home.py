from flask import Blueprint, render_template, request, session, redirect, url_for
from ..models.flight import Flight
from ..models.booking import Booking
from ..models.register import Register
from ..helpers.parse_data_helpers import md5_hash
from datetime import timedelta

bp = Blueprint('home', __name__)
@bp.route("/")
def home():
    user_id = session.get("user_id")  
    usertype = session.get("usertype")  
    booking = Booking(None, None, [], None, [], Flight(), Flight())
    return render_template("parse_data.html", booking=booking, user_id=user_id, usertype=usertype)
@bp.route("/admin", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        hashed_password = md5_hash(password)
        user = Register.query.filter_by(email=email, password=hashed_password, usertype="admin").first()
        
        if user:
            session["user_id"] = user.id
            session["usertype"] = "admin"
            return redirect(url_for("home.admin_infopayment"))
        else:
            error = "Email hoặc mật khẩu không đúng"
            return render_template("admin/login.html", error=error)
    
    return render_template("admin/login.html")

@bp.route("/admin/infopayment")
def admin_infopayment():
    if session.get("usertype") != "admin":
        return redirect(url_for("home.admin_login"))
    return render_template("admin/infopayment.html")
@bp.route("/admin/infopackage")
def admin_infopackage():
    if session.get("usertype") != "admin":
        return redirect(url_for("home.admin_login"))
    return render_template("admin/infopackage.html")
@bp.route("/admin/subscription")
def admin_subscription():
    if session.get("usertype") != "admin":
        return redirect(url_for("home.admin_login"))
    return render_template("admin/subscription.html")