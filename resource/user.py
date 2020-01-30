from flask_restful import Resource, reqparse
from flask_login import login_user, logout_user, current_user, login_required
from flask_jwt import jwt_required
from models.user import UserModel

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

        if data['username'] == 'admin':
            user = UserModel(data['username'],data['password'],2)
        else:
            user = UserModel(data['username'],data['password'],0)

        user.save_to_db()
        return {'message':'Successfully created.'}, 201


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
        if not current_user.is_authenticated:
            data = LoginUser.parser.parse_args()
            user = UserModel.query.filter_by(username=data['username']).first()
            if user and user.check_pass(data['password']):
                login_user(user)
                return {'message':'Log in successfully.'}, 200
            return {'message':"This user doesn't exists."}, 400
        return {'message':'This user already authenticated.'}, 400

class LogoutUser(Resource):
    def post(self):
        logout_user()
        return {'message':'Log out successfully.'}, 200

class MakeDispatcher(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('license',
                        type=int,
                        required=True,
                        help='This field cannot be blank.')

    #@jwt_required()
    @login_required
    def put(self, username):
        if current_user.username == 'admin':
            data = MakeDispatcher.parser.parse_args()
            user = UserModel.query.filter_by(username=username).first()
            if user and user.username != 'admin' and data['license'] in [1,2,3]:
                user.license = data['license']
                user.save_to_db()
                return {'message':'Successfully updated.'}, 200
            return {'message':'User not found or wrong input information.'}, 400
        return {'message':'Access denied.'}, 403
