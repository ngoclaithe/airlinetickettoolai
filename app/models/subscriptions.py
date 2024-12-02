from app.extensions import db
from datetime import datetime, date

class Subscription(db.Model):
    __tablename__ = 'subscriptions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('register.id'), nullable=False, unique=False)
    start_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    end_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='waiting')  
    code_paymment = db.Column(db.String, nullable=True)  
    user = db.relationship('Register', back_populates='subscriptions')

    def as_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'status': self.status,
            'code_paymment': self.code_paymment
        }    

    @staticmethod
    def get_all_subscription():
        subscriptions = Subscription.query.all()
        return [subscription.as_dict() for subscription in subscriptions]    

    def add_subscription(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_subscription_by_user_id(user_id):
        return Subscription.query.filter_by(user_id=user_id).first()

    @staticmethod
    def update_subscription(user_id, start_date=None, end_date=None, status=None):
        subscription = Subscription.query.filter_by(user_id=user_id).first()
        if subscription:
            if start_date:
                subscription.start_date = start_date
            if end_date:
                subscription.end_date = end_date
            if status:
                subscription.status = status  
            db.session.commit()
        return subscription
    @staticmethod
    def update_subscription_by_code(code_paymment):
        status = "success"
        subscription = Subscription.query.filter_by(code_paymment=code_paymment).first()
        if subscription:
            if status:
                subscription.status = status  
            db.session.commit()
        return subscription
    @staticmethod
    def delete_subscription(user_id):
        subscription = Subscription.query.filter_by(user_id=user_id).first()
        if subscription:
            db.session.delete(subscription)
            db.session.commit()
        return subscription
    @staticmethod
    def is_registered(user_id):
        subscription = Subscription.query.filter_by(user_id=user_id).first()
        if subscription:
            today = date.today()
            if subscription.start_date <= today <= subscription.end_date and subscription.status == "success":
                return True
        return False
