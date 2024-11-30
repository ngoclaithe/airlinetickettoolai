from app.extensions import db
from sqlalchemy import Integer, String

class Session(db.Model):
    __tablename__ = 'sessions'

    id = db.Column(Integer, primary_key=True)
    session_id = db.Column(String(255), unique=True)
    data = db.Column(db.Text)
    expiry = db.Column(db.DateTime)

    def __repr__(self):
        return f"<Session {self.session_id}>"
