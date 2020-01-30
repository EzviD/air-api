from flask_restful import Resource, reqparse
from models.airoports import AiroportsModel
from flask_jwt import jwt_required
from flask_login import login_required, current_user

class Airoport(Resource):
    def get(self, country, city, tag):
        airoport = AiroportsModel.find_airoport(country,city,tag)

        if airoport:
            return airoport.json()
        return {'message':'Airoport not found'}, 404

    #@jwt_required()
    @login_required
    def post(self, country, city, tag):
        if current_user.username == 'admin':
            if AiroportsModel.find_airoport(country,city,tag):
                return {'message':'Airoport already exists.'}, 400
            try:
                airoport = AiroportsModel(country,city,tag)
                airoport.save_to_db()
                return {'message':'Created successfully.'}, 201
            except:
                return {"message": "An error occurred inserting the item."}, 500
        return {'message':'Access denied.'}, 403

    #@jwt_required()
    @login_required
    def delete(self, country, city, tag):
        if current_user.username == 'admin':
            airoport = AiroportsModel.find_airoport(country,city,tag)

            if airoport:
                airoport.delete_from_db()
                return {'message':'Successfully deleted.'}, 200
            return {'message':"Airoport doesn't exists."}, 400
        return {'message':'Access denied.'}, 403


class AiroportList(Resource):
    def get(self):
        return {'airoports':list(map(lambda x: x.json(), AiroportsModel.query.all()))}
