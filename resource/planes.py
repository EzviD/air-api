from flask_restful import Resource, reqparse
from models.planes import PlaneModel
from models.user import UserModel
from models.airoports import AiroportsModel
from flask_jwt_extended import jwt_required, get_jwt_identity

class Plane(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('airoport_tag',
                    type=str,
                    required=True,
                    help='This field cannot be blank.')

    def get(self, name):
        plane = PlaneModel.find_by_name(name)

        if plane:
            return plane.json()
        return {'message':"Plane not found."}, 404

    @jwt_required
    def post(self, name):
        user_id = get_jwt_identity()
        current_user = UserModel.find_by_id(user_id)
        if current_user.license in [1,2]:
            data = Plane.parser.parse_args()

            if PlaneModel.find_by_name(name):
                return {'message':'Plane already exists'}, 400
            plane = PlaneModel(name, data['airoport_tag'])
            try:
                plane.save_to_db()
                return {'message':'Successfully created.'}, 201
            except:
                return {"message": "An error occurred inserting the item."}, 500
        return {'message':'Access denied.'}, 403

    @jwt_required
    def delete(self, name):
        user_id = get_jwt_identity()
        current_user = UserModel.find_by_id(user_id)
        if current_user.license in [1,2]:
            plane = PlaneModel.find_by_name(name)

            if plane:
                plane.delete_from_db()
                return {'message':'Successfully deleted.'}, 200
            return {'message':'Plane not found.'}, 404
        return {'message':'Access denied.'}, 403

    @jwt_required
    def put(self, name):
        user_id = get_jwt_identity()
        current_user = UserModel.find_by_id(user_id)
        if current_user.license in [1,2]:
            data = Plane.parser.parse_args()
            plane = PlaneModel.find_by_name(name)

            if plane:
                if AiroportsModel.find_airoport(data['airoport_tag']) is not None:
                    plane.airoport_tag = data['airoport_tag']
                else:
                    return {'message':"This tag doesn't exist."}, 404
            else:
                plane = PlaneModel(name, data['airoport_tag'])

            plane.save_to_db()
            return plane.json()
        return {'message':'Access denied.'}, 403


class PlaneList(Resource):
    def get(self):
        return {'planes':list(map(lambda x: x.json(), PlaneModel.query.all()))}
