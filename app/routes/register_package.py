from flask import (
    Blueprint,
    render_template,
    request,
    session,
    redirect,
    url_for,
    current_app,
    jsonify,
)
from ..models.register import Register
from ..models.info_package import InfoPackage
from ..models.subscriptions import Subscription
from ..models.infopayment import InfoPayment
from ..helpers.parse_data_helpers import md5_hash
from ..helpers.number_manager import *
from datetime import datetime, timedelta

bp = Blueprint("register_package", __name__)


@bp.route("/register_menu", methods=["GET"])
def register_menu():
    if "user_id" in session and session["usertype"] in ["admin", "guest"]:
        user_id = session.get("user_id")
        user = Register.query.filter_by(id=session["user_id"]).first()
        if user:
            return render_template(
                "register_package.html", user_name=user.user, user_id=user_id
            )
        else:
            return "Không tìm thấy thông tin người dùng", 404
    else:
        return redirect(url_for("auth_blueprint.login"))


@bp.route("/get_all_package", methods=["GET"])
def get_all_package():
    packages = InfoPackage.get_all_packages()
    return jsonify(packages)
@bp.route("/get_all_subscription", methods=["GET"])
def get_all_subscription():
    subscriptions = Subscription.get_all_subscription()
    return jsonify(subscriptions)


@bp.route("/update_package", methods=["POST"])
def update_package():
    if "user_id" in session and session["usertype"] in ["admin", "guest"]:
        price = request.json.get("price")
        id = request.json.get("id")
        # info_packages = InfoPackage()
        info_packages = InfoPackage.update_price_by_id(id,price)
    return jsonify(info_packages), 200
@bp.route("/accept_subscription", methods=["POST"])
def accept_subscription():
    if "user_id" in session and session["usertype"] in ["admin", "guest"]:
        code_paymment = request.json.get("code_paymment")
        print("gia tri trong form code", code_paymment)
        subscription= Subscription.update_subscription_by_code(code_paymment)
        return (jsonify({"message": "Chấp nhận đăng ký gói thành công"}),200,)
    else:
        return redirect(url_for("auth_blueprint.login"))

@bp.route("/select_subscription", methods=["POST"])
def select_subscription():
    if "user_id" in session and session["usertype"] in ["admin", "guest"]:
        package_id = int(request.json.get("package_id", 0))
        info = request.json.get("info")
        print("gia tri backend", package_id)
        user_id = session.get("user_id")
        today = datetime.utcnow()
        start_date = today
        if package_id == 1:
            end_date = start_date + timedelta(days=7)
        elif package_id == 2:
            end_date = start_date + timedelta(days=30)
        elif package_id == 3:
            end_date = start_date + timedelta(days=30 * 6)
        elif package_id == 4:
            end_date = start_date + timedelta(days=365)
        else:
            return jsonify({"error": "Gói không hợp lệ"}), 400

        subscription = Subscription(
            user_id=user_id,
            start_date=start_date,
            end_date=end_date,
            status="waiting",
            code_paymment=info,
        )
        subscription.add_subscription()
        return (
            jsonify(
                {
                    "message": "Đăng ký gói thành công",
                    "start_date": start_date.strftime("%Y-%m-%d"),
                    "end_date": end_date.strftime("%Y-%m-%d"),
                    "status": "waiting",
                }
            ),
            200,
        )
    else:
        return redirect(url_for("auth_blueprint.login"))


@bp.route("/get_all_info_payment", methods=["GET"])
def get_all_info_payment():
    info_paymments = InfoPayment.get_all_info_paymment()
    return jsonify(info_paymments)


@bp.route("/add_info_payment", methods=["POST"])
def add_info_payment():
    if "user_id" in session and session["usertype"] in ["admin", "guest"]:
        bank_account_number = request.json.get("bank_account_number")
        bank_account_name = request.json.get("bank_account_name")
        bank = request.json.get("bank")
        info_paymments = InfoPayment().add_info_paymment(bank_account_number, bank_account_name, bank)
    return jsonify(info_paymments), 200
@bp.route("/delete_info_payment", methods=["POST"])
def delete_info_payment():
    if "user_id" in session and session["usertype"] in ["admin", "guest"]:
        bank_account_number = request.json.get("bank_account_number")
        info_payment = InfoPayment.delete_info_payment(bank_account_number)
        if info_payment:
            return jsonify(info_payment.as_dict()), 200 
        else:
            return jsonify({"message": "Không tìm thấy thông tin thanh toán"}), 404
