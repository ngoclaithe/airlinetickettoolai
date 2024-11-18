from app.extensions import db
class Register(db.Model):
    __tablename__ = 'register'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    usertype = db.Column(db.String(20), nullable=False)
    secret_question = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255), nullable=True)

    def add_register(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all_registers():
        return Register.query.all()

    @staticmethod
    def find_by_email(email):
        return Register.query.filter_by(email=email).first()

    @staticmethod
    def update_register(id, user=None, email=None, password=None, usertype=None, secret_question=None, phone=None):
        register = Register.query.get(id)
        if register:
            if user:
                register.user = user
            if email:
                register.email = email
            if password:
                register.password = password
            if usertype:
                register.usertype = usertype
            if secret_question:
                register.secret_question = secret_question
            if phone:
                register.phone = phone
            db.session.commit()
        return register

    @staticmethod
    def delete_register(id):
        register = Register.query.get(id)
        if register:
            db.session.delete(register)
            db.session.commit()
        return register
