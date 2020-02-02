from flask import jsonify
from app import app, jwt
from db import db
from models.user import UserModel
from blacklist import BLACKLIST

db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:
        return {'is_admin':True}
    return {'is_admin':False}

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST

@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'description': 'The token has expired.',
        'error': 'token_expired'
    }), 401

@jwt.invalid_token_loader
def invalid_token_callback(x):
    return jsonify({
        'description': 'Invalid token.',
        'error': 'token_invalid'
    }), 401

@jwt.unauthorized_loader
def unauthorized_token_callback():
    return jsonify({
        'description': 'Unathorized.',
        'error': 'unathorized_token'
    }), 401

@jwt.needs_fresh_token_loader
def needs_fresh_token_callback():
    return jsonify({
        'description': 'Need fresh token.',
        'error': 'needs_fresh_token'
    }), 401

@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        'description': 'Revoked token.',
        'error': 'revoked_token'
    }), 401
