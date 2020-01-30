from db import db

class TimetableModel(db.Model):
    __tablename__ = 'timetable'

    id = db.Column(db.Integer, primary_key=True)
    startpoint = db.Column(db.String)
    endpoint = db.Column(db.String)
    departure_time = db.Column(db.String)

    plane_name = db.Column(db.String, db.ForeignKey('planes.name'))
    plane = db.relationship('PlaneModel')

    def __init__(self, startpoint, endpoint, departure_time, plane_name):
        self.startpoint = startpoint
        self.endpoint = endpoint
        self.departure_time = departure_time
        self.plane_name = plane_name

    def json(self):
        return {'id':self.id, 'route':f'{self.startpoint} - {self.endpoint}','departure_time':self.departure_time}

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_timetable(cls, startpoint, endpoint, departure_time):
        return cls.query.filter_by(startpoint=startpoint, endpoint=endpoint, departure_time=departure_time).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
