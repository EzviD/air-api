import os
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from models.user import UserModel
from blacklist import BLACKLIST
from resource.user import UserRegister, LoginUser, LogoutUser, User, TokenRefresh, MakeDisp, Users
from resource.airoports import Airoport, AiroportList
from resource.planes import Plane, PlaneList
from resource.timetable import Timetable, TimeableList

app = Flask(__name__)
jwt = JWTManager(app)
api = Api(app)
basedir = os.path.abspath(os.path.dirname(__file__))
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=['2 per second']
)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///'+os.path.join(basedir, 'data.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTION'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access','refresh']
app.config['SECRET_KEY'] = '*'
app.config['JWT_SECRET_KEY'] = '*'

api.add_resource(TimeableList, '/timetables')
api.add_resource(Timetable, '/timetable')
api.add_resource(PlaneList, '/planes')
api.add_resource(Plane, '/plane/<string:name>')
api.add_resource(AiroportList, '/airoports')
api.add_resource(Airoport, '/airoport/<string:country>/<string:city>/<string:tag>')
api.add_resource(MakeDisp, '/disp/id<int:user_id>')
api.add_resource(User, '/user/id<int:user_id>')
api.add_resource(Users, '/users')
api.add_resource(LoginUser, '/login')
api.add_resource(LogoutUser, '/logout')
api.add_resource(UserRegister, '/register')
api.add_resource(TokenRefresh, '/refresh')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000,debug=True)
