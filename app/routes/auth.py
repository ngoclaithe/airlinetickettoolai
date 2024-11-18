from flask import Blueprint, render_template, request, session, redirect, url_for, current_app
from ..models.register import Register
from ..helpers.parse_data_helpers import md5_hash

bp = Blueprint('auth', __name__)

@bp.route("/login_page")
def login_page():
    return render_template("login.html")

@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = md5_hash(request.form["password"])
        user = Register.query.filter_by(email=email, password=password).first()

        if user:
            session["user_id"] = user.id
            session["usertype"] = user.usertype
            session.permanent = True
            
            if user.usertype == "admin":
                return redirect(url_for("admin.overview"))
            elif user.usertype == "guest":
                return redirect(url_for("booking_blueprint.parse_page"))
        else:
            return "Notok", 400
    return render_template("login.html")

@bp.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return render_template("login.html")