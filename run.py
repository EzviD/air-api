from app import app, login_manager
from db import db

db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return db.session.query(UserModel).get(user_id)
