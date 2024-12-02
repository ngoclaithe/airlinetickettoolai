from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify
from ..models.register import Register
from ..helpers.text_manager import TextManager  

bp = Blueprint('uppertext', __name__)

def check_user_authentication():

    if "user_id" not in session or session["usertype"] not in ["admin", "guest"]:
        return redirect(url_for("auth_blueprint.login"))
    
    user = Register.query.filter_by(id=session["user_id"]).first()
    if not user:
        return "Không tìm thấy thông tin người dùng", 404
    
    return user

@bp.route("/uppertext", methods=["GET"])
def number_tool():
    user_result = check_user_authentication()
    if isinstance(user_result, tuple):
        return user_result
    
    return render_template("uppertext.html", user_name=user_result.user, user_id=user_result.id)

@bp.route("/convert_text", methods=["POST"])
def convert_text():
    user_result = check_user_authentication()
    if isinstance(user_result, tuple):
        return user_result
    text = request.form.get('dataNumberToText', '')
    conversion_type = request.form.get('conversion_type', '')
    text_manager = TextManager(text)
    result = ""
    if conversion_type == 'uppercase':
        result = text_manager.to_uppercase()
    elif conversion_type == 'lowercase':
        result = text_manager.to_lowercase()
    elif conversion_type == 'titlecase':
        result = text_manager.title_case()
    elif conversion_type == 'swapcase':
        result = text_manager.swap_case()
    else:
        return jsonify({"error": "Loại chuyển đổi không hợp lệ"}), 400
    return jsonify({"result": result})