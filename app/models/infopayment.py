from app.extensions import db
from datetime import datetime, date

class InfoPayment(db.Model):
    __tablename__ = 'info_paymment'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bank_account_number = db.Column(db.Integer, nullable=False)
    bank_account_name = db.Column(db.String, nullable=False)
    bank = db.Column(db.String, nullable=False)
    def as_dict(self):
        return {
            'id': self.id,
            'bank_account_number': self.bank_account_number,
            'bank_account_name': self.bank_account_name, 
            'bank': self.bank
        }       
    @staticmethod        
    def add_info_paymment(bank_account_number, bank_account_name, bank):
        new_payment = InfoPayment(
            bank_account_number=bank_account_number,
            bank_account_name=bank_account_name,
            bank=bank
        )
        db.session.add(new_payment)
        db.session.commit()

    @staticmethod
    def get_all_info_paymment():
        infopayments = InfoPayment.query.all()
        return [infopayment.as_dict() for infopayment in infopayments]

    @staticmethod
    def delete_info_payment(bank_account_number):
        info_payment = InfoPayment.query.filter_by(bank_account_number=bank_account_number).first()
        if info_payment:
            db.session.delete(info_payment)
            db.session.commit()
        return info_payment
