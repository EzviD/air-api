from flask import jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required,
    get_raw_jwt,
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    fresh_jwt_required,
    get_jwt_identity,
    get_jwt_claims
)
from models.user import UserModel
from blacklist import BLACKLIST


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help='This field cannot be blank.')
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help='This field cannot be blank.')

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message':'This user already exists.'}, 400

        try:
            if data['username'] == 'admin':
                user = UserModel(data['username'],data['password'],2)
            else:
                user = UserModel(data['username'],data['password'],0)
                user.save_to_db()
                return {'message':'Successfully created.'}, 201
        except:
            return {"message": "An error occurred inserting the item."}, 500


class LoginUser(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help='This field cannot be blank.')
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help='This field cannot be blank.')

    def post(self):
        data = LoginUser.parser.parse_args()
        user = UserModel.query.filter_by(username=data['username']).first()
        if user and user.check_pass(data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token':access_token,
                'refresh_token':refresh_token
            }, 200

class LogoutUser(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        BLACKLIST.add(jti)
        return {'message':'Log out successfully.'}, 200

class User(Resource):

    @jwt_required
    def get(self,user_id):
        claims = get_jwt_claims()
        if claims['is_admin']:
            user = UserModel.find_by_id(user_id)
            if not user:
                return {'message':'User not found.'}, 404
            return user.json()

    @fresh_jwt_required
    def delete(self,user_id):
        claims = get_jwt_claims()
        if claims['is_admin']:
            user = UserModel.find_by_id(user_id)
            if user and user.id != 1:
                user.delete_from_db()
                return {'message':'Successfully deleted.'}, 200
            return {'message':'User not found.'}, 404
        return {'message':'Access denied.'}, 403

class Users(Resource):
    @jwt_required
    def get(self):
        claims = get_jwt_claims()
        if claims['is_admin']:
            return {'users':[user.json() for user in UserModel.query.all()]}

class MakeDisp(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('license',
                        type=int,
                        required=True,
                        help='This field cannot be blank.')

    @jwt_required
    def put(self, user_id):
        claims = get_jwt_claims()
        if claims['is_admin']:
            data = MakeDisp.parser.parse_args()
            user = UserModel.query.filter_by(id=user_id).first()
            if user and user.id != 1 and data['license'] in [0,1]:
                user.license = data['license']
                user.save_to_db()
                return {'message':'Successfully updated.'}, 200
            return {'message':'User not found or wrong input information.'}, 400
        return {'message':'Access denied.'}, 403

class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}
