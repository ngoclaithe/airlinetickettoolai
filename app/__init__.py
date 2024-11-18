from flask import Flask
from app.extensions import db
from app.routes import home, booking, auth, numbertool, register_package
from datetime import timedelta

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)
    db.init_app(app)

    app.register_blueprint(home.bp)
    app.register_blueprint(booking.bp, name='booking_blueprint')
    app.register_blueprint(auth.bp, name='auth_blueprint')
    app.register_blueprint(numbertool.bp)
    app.register_blueprint(register_package.bp)
    return app
