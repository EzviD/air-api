from db import db

class AiroportsModel(db.Model):
    __tablename__ = 'airoports'

    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String, unique=True, nullable=False)
    country = db.Column(db.String, unique=False, nullable=False)
    city = db.Column(db.String, unique=False, nullable=False)

    planes = db.relationship('PlaneModel', lazy='dynamic')

    def __init__(self,country,city,tag):
        self.country = country
        self.city = city
        self.tag = tag

    def json(self):
        return {'country':self.country, 'city':self.city,'tag':self.tag,'planes':[plane.json() for plane in self.planes.all()]}

    @classmethod
    def find_airoport(cls, tag):
        return cls.query.filter_by(tag=tag).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
