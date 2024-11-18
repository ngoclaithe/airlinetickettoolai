from flask import Blueprint, render_template, request, session, redirect, url_for, current_app, jsonify
from ..models.register import Register
from ..helpers.parse_data_helpers import md5_hash
from ..helpers.number_manager import *

bp = Blueprint('register_package', __name__)

@bp.route("/register_menu", methods=["GET"])
def register_menu():
    if "user_id" in session and session["usertype"] in ["admin", "guest"]:
        user_id = session.get("user_id")  
        user = Register.query.filter_by(id=session["user_id"]).first()
        if user:
            return render_template("register_package.html", user_name=user.user, user_id=user_id)
        else:
            return "Không tìm thấy thông tin người dùng", 404
    else:
        return redirect(url_for("auth_blueprint.login"))
