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