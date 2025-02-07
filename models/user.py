from db import db
from werkzeug.security import generate_password_hash, check_password_hash

class UserModel(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    hash_pass = db.Column(db.String)
    license = db.Column(db.Integer, default=0) #dispatchers

    def __init__(self,username,password,license):
        self.username = username
        self.set_pass(password)
        self.license = license

    def json(self):
        return {'id':self.id, 'username': self.username, 'license': self.license}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def set_pass(self,password):
        self.hash_pass = generate_password_hash(password)

    def check_pass(self,password):
        return check_password_hash(self.hash_pass, password)
