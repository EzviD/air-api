from flask_restful import Resource, reqparse
from models.timetable import TimetableModel
from models.user import UserModel
from flask_jwt_extended import jwt_required, get_jwt_identity

class Timetable(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('startpoint',
                        type=str,
                        required=False,
                        help='This field cannot be blank.')
    parser.add_argument('endpoint',
                        type=str,
                        required=True,
                        help='This field cannot be blank.')
    parser.add_argument('departure_time',
                        type=str,
                        required=True,
                        help='This field cannot be blank.')
    parser.add_argument('plane_name',
                        type=str,
                        required=True,
                        help='This field cannot be blank')

    def get(self):
        data = Timetable.parser.parse_args()
        if data['startpoint']:
            startpoint = data['startpoint']
        else:
            startpoint = TimetableModel.find_plane_airoport(data['plane_name'])
        time = TimetableModel.query.filter_by(startpoint=startpoint,
        endpoint=data['endpoint'],departure_time=data['departure_time'],
        plane_name=data['plane_name']).first()

        if time:
            return time.json()
        return {'message':'Timetable not found.'}, 404

    @jwt_required
    def post(self):
        user_id = get_jwt_identity()
        current_user = UserModel.find_by_id(user_id)
        if current_user.license in [1,2]:
            data = Timetable.parser.parse_args()
            if data['startpoint']:
                startpoint = data['startpoint']
            else:
                startpoint = TimetableModel.find_plane_airoport(data['plane_name'])
            time = TimetableModel.query.filter_by(startpoint=startpoint,
            endpoint=data['endpoint'],departure_time=data['departure_time'],
            plane_name=data['plane_name']).first()

            if time:
                return {'message':'This timetable already exists.'}, 400
            try:
                time = TimetableModel(startpoint=startpoint,
                endpoint=data['endpoint'],departure_time=data['departure_time'],
                plane_name=data['plane_name'])
                time.save_to_db()
                return {'message':'Successfully created.'}, 200
            except:
                return {"message": "An error occurred inserting the item."}, 500
        return {'message':'Access denied.'}, 403

    @jwt_required
    def delete(self):
        user_id = get_jwt_identity()
        current_user = UserModel.find_by_id(user_id)
        if current_user.license in [1,2]:
            data = Timetable.parser.parse_args()
            if data['startpoint']:
                startpoint = data['startpoint']
            else:
                startpoint = TimetableModel.find_plane_airoport(data['plane_name'])
            time = TimetableModel.query.filter_by(startpoint=startpoint,
            endpoint=data['endpoint'],departure_time=data['departure_time'],
            plane_name=data['plane_name']).first()

            if time:
                time.delete_from_db()
                return {'message':'Successfully deleted.'}, 200
            return {'message':'Timetable not found.'}, 404
        return {'message':'Access denied.'}, 403


class TimeableList(Resource):
    def get(self):
        return {'timetables':list(map(lambda x: x.json(), TimetableModel.query.all()))}
