from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify
from ..models.register import Register
from ..helpers.parse_data_helpers import md5_hash

bp = Blueprint('auth', __name__)

@bp.route("/login_page")
def login_page():
    return render_template("login.html")

@bp.route("/info_account", methods=["GET"])
def info_account():
    user_id = session["user_id"] 
    user_name = session["user_name"]
    user_type = session["usertype"]
    email = session["email"]
    return render_template("account.html", user_name = user_name, user_type = user_type, email = email, user_id = user_id )

@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = md5_hash(request.form["password"])
        user = Register.query.filter_by(email=email, password=password).first()

        if user:
            session["user_id"] = user.id
            session["user_name"] = user.user
            session["usertype"] = user.usertype
            session["email"] = user.email
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

@bp.route("/register", methods=["POST"])
def register_account():
    try:
        data = request.json
        user = data.get("user")
        email = data.get("email")
        password = data.get("password")
        usertype = data.get("usertype")
        secret_question = data.get("secret_question")
        phone = data.get("phone")

        if Register.find_by_email(email):
            return jsonify({"error": "Email đã được sử dụng"}), 400

        hashed_password = md5_hash(password)
        new_user = Register(
            user=user,
            email=email,
            password=hashed_password,
            usertype=usertype,
            secret_question=secret_question,
            phone=phone
        )
        new_user.add_register()
        return jsonify({"message": "Tạo tài khoản thành công"}), 201
    except Exception as e:
        # db.session.rollback()
        return jsonify({"error": str(e)}), 500