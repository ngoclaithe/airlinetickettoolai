from app.extensions import db
from datetime import datetime, date

class InfoPackage(db.Model):
    __tablename__ = 'infopackage'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name_package = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Integer, nullable=False)  
    def as_dict(self):
        return {
            'id': self.id,
            'name_package': self.name_package,
            'price': self.price
        }    
    @staticmethod
    def update_price_by_id(package_id, new_price):
        package = InfoPackage.query.get(package_id)
        if package:
            package.price = new_price
            db.session.commit()
            return True
        return False

    @staticmethod
    def get_all_packages():
        packages = InfoPackage.query.all()
        return [package.as_dict() for package in packages]

    @staticmethod
    def get_price_by_id(package_id):
        package = InfoPackage.query.get(package_id)
        if package:
            return package.price
        return None
