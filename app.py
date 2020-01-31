import os
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from flask_login import LoginManager

from security import authenticate, identity
from models.user import UserModel
from resource.user import UserRegister, LoginUser, LogoutUser, MakeDispatcher
from resource.airoports import Airoport, AiroportList
from resource.planes import Plane, PlaneList
from resource.timetable import Timetable, TimeableList

app = Flask(__name__)
jwt = JWT(app, authenticate, identity)
api = Api(app)
login_manager = LoginManager(app)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTION'] = True
app.config['SECRET_KEY'] = '*'
app.config['JWT_SECRET_KEY'] = '*'

@login_manager.user_loader
def load_user(user_id):
    return db.session.query(UserModel).get(user_id)

api.add_resource(TimeableList, '/timetables')
api.add_resource(Timetable, '/timetable')
api.add_resource(PlaneList, '/planes')
api.add_resource(Plane, '/plane/<string:name>')
api.add_resource(AiroportList, '/airoports')
api.add_resource(Airoport, '/airoport/<string:country>/<string:city>/<string:tag>')
api.add_resource(MakeDispatcher, '/disp/<string:username>')
api.add_resource(LoginUser, '/login')
api.add_resource(LogoutUser, '/logout')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000,debug=True)
