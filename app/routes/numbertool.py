from flask import Blueprint, render_template, request, session, redirect, url_for, current_app, jsonify
from ..models.register import Register
from ..helpers.parse_data_helpers import md5_hash
from ..helpers.number_manager import *

bp = Blueprint('numbertool', __name__)

@bp.route("/numbertool", methods=["GET"])
def number_tool():
    if "user_id" in session and session["usertype"] in ["admin", "guest"]:
        user_id = session.get("user_id")  
        user = Register.query.filter_by(id=session["user_id"]).first()
        if user:
            return render_template("number.html", user_name=user.user, user_id=user_id)
        else:
            return "Không tìm thấy thông tin người dùng", 404
    else:
        return redirect(url_for("auth_blueprint.login"))

@bp.route("/numbertotext", methods=["POST"])
def number_to_text():
    if "user_id" in session and session["usertype"] in ["admin", "guest"]:
        user_id = session.get("user_id")  
        user = Register.query.filter_by(id=session["user_id"]).first()
        print("Số nhận được từ form", request.form)
        number = request.form.get("dataNumberToText")

        if not number:
            return jsonify({"error": "Dữ liệu không hợp lệ: Vui lòng nhập số để chuyển đổi."}), 400

        if user:
            try:
                numbermanager = NumberManager()
                data = numbermanager.convert_number_to_words(number)
                return jsonify({"result": data})
            except Exception as e:
                return jsonify({"error": f"Đã xảy ra lỗi khi chuyển đổi số: {str(e)}"}), 500
        else:
            return jsonify({"error": "Không tìm thấy thông tin người dùng"}), 404
    else:
        return redirect(url_for("auth_blueprint.login"))

@bp.route("/cacul_VAT", methods=["POST"])
def cacul_VAT():
    if "user_id" in session and session["usertype"] in ["admin", "guest"]:
        user_id = session.get("user_id")  
        user = Register.query.filter_by(id=session["user_id"]).first()

        numberVAT = request.form.get("numberVAT")
        percentVAT = request.form.get("%VAT")
        VATType = request.form.get("VATType")

        print("Du lieu number", numberVAT)
        print("Kiểu VAT", VATType)

        if not numberVAT or not percentVAT or not VATType:
            return jsonify({"error": "Dữ liệu không hợp lệ: Vui lòng nhập đầy đủ thông tin VAT."}), 400

        try:
            numbermanager = NumberManager()
            data = None
            if VATType == "VATxuoi":
                data = numbermanager.calculate_vat_forward(int(numberVAT), int(percentVAT))
            elif VATType == "VATnguoc":
                data = numbermanager.calculate_vat_reverse(int(numberVAT), int(percentVAT))
            else:
                return jsonify({"error": "Kiểu VAT không hợp lệ."}), 400

            return jsonify({"result": data})
        except Exception as e:
            return jsonify({"error": f"Đã xảy ra lỗi khi tính toán VAT: {str(e)}"}), 500
        else:
            return jsonify({"error": "Không tìm thấy thông tin người dùng"}), 404
    else:
        return redirect(url_for("auth_blueprint.login"))
