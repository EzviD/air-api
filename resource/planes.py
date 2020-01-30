from flask_restful import Resource, reqparse
from models.planes import PlaneModel
from flask_jwt import jwt_required
from flask_login import login_required, current_user

class Plane(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('airoport_tag',
                        type=str,
                        required=True,
                        help='This field cannot be blank.')

    def get(self, name):
        data = Plane.parser.parse_args()
        plane = PlaneModel.find_plane(name, data['airoport_tag'])

        if plane:
            return plane.json()
        return {'message':"Plane not found."}, 404

    #@jwt_required()
    @login_required
    def post(self, name):
        if current_user.license in [1,2]:
            data = Plane.parser.parse_args()

            if PlaneModel.find_plane(name, data['airoport_tag']):
                return {'message':'Plane already exists'}, 400
            plane = PlaneModel(name, data['airoport_tag'])
            try:
                plane.save_to_db()
                return {'message':'Successfully created.'}, 201
            except:
                return {"message": "An error occurred inserting the item."}, 500
        return {'message':'Access denied.'}, 403

    #@jwt_required()
    @login_required
    def delete(self, name):
        if current_user.license in [1,2]:
            plane = PlaneModel.query.filter_by(name=name).first()

            if plane:
                plane.delete_from_db()
                return {'message':'Successfully deleted.'}, 200
            return {'message':'Plane not found.'}, 404
        return {'message':'Access denied.'}, 403

    #@jwt_required()
    @login_required
    def put(self, name):
        if current_user.license in [1,2]:
            data = Plane.parser.parse_args()
            plane = PlaneModel.find_plane(name, data['airoport_tag'])

            if plane:
                plane.airoport_tag = data['airoport_tag']
            else:
                plane = PlaneModel(name, data['airoport_tag'])

            plane.save_to_db()
            return plane.json()
        return {'message':'Access denied.'}, 403


class PlaneList(Resource):
    def get(self):
        return {'planes':list(map(lambda x: x.json(), PlaneModel.query.all()))}
