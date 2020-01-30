from db import db

class PlaneModel(db.Model):
    __tablename__ = 'planes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)

    airoport_tag = db.Column(db.String, db.ForeignKey('airoports.tag'))
    airoport = db.relationship('AiroportsModel')

    timetables = db.relationship('TimetableModel', lazy='dynamic')


    def __init__(self, name, airoport_tag):
        self.name = name
        self.airoport_tag = airoport_tag

    def json(self):
        return {'name':self.name,'airoport':self.airoport_tag,'timetables':[time.json() for time in self.timetables]}

    @classmethod
    def find_plane(cls, name, tag):
        return cls.query.filter_by(name=name, airoport_tag=tag).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
