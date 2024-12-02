from flask import Flask
from flask_session import Session
from app.extensions import db
from app.routes import home, booking, auth, numbertool, register_package, uppertext
from datetime import timedelta
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)

    app.config['SESSION_TYPE'] = 'sqlalchemy'
    app.config['SESSION_SQLALCHEMY'] = db  
    app.config['SESSION_SQLALCHEMY_TABLE'] = 'sessions'  

    db.init_app(app)
    Session(app)
    
    with app.app_context():
        db.create_all() 

    app.register_blueprint(home.bp)
    app.register_blueprint(booking.bp, name='booking_blueprint')
    app.register_blueprint(auth.bp, name='auth_blueprint')
    app.register_blueprint(numbertool.bp)
    app.register_blueprint(uppertext.bp)
    app.register_blueprint(register_package.bp)

    return app
