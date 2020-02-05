from flask_restful import Resource, reqparse
from models.airoports import AiroportsModel
from flask_jwt_extended import jwt_required, fresh_jwt_required, get_jwt_identity, get_jwt_claims

class Airoport(Resource):
    def get(self, country, city, tag):
        airoport = AiroportsModel.find_airoport(tag)

        if airoport:
            return airoport.json()
        return {'message':'Airoport not found'}, 404

    @jwt_required
    def post(self, country, city, tag):
        claims = get_jwt_claims()
        if claims['is_admin']:
            if AiroportsModel.find_airoport(tag):
                return {'message':'Airoport already exists.'}, 400
            try:
                airoport = AiroportsModel(country,city,tag)
                airoport.save_to_db()
                return {'message':'Created successfully.'}, 201
            except:
                return {"message": "An error occurred inserting the item."}, 500
        return {'message':'Access denied.'}, 403

    @fresh_jwt_required
    def delete(self, country, city, tag):
        claims = get_jwt_claims()
        if claims['is_admin']:
            airoport = AiroportsModel.find_airoport(tag)

            if airoport:
                airoport.delete_from_db()
                return {'message':'Successfully deleted.'}, 200
            return {'message':"Airoport doesn't exists."}, 400
        return {'message':'Access denied.'}, 403


class AiroportList(Resource):
    def get(self):
        return {'airoports':list(map(lambda x: x.json(), AiroportsModel.query.all()))}
