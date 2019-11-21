from flask import Blueprint, jsonify, request
import flask_jwt_extended as jwt

from service.models import db, User

from service.utility import errors
import json
auth = Blueprint('auth', __name__)

BP_ID = 2

@auth.route('/login', methods=['POST'])
def login(func_id=0):
    '''
    Performs the check of the credentials of a user.
    '''

    user_cred = json.loads(request.get_json())
    user = User.query.filter_by(username=user_cred['username']).one_or_none()

    if user is None:
        return errors.response(f'{BP_ID}{func_id}1')
    
    if not user.authenticate(user_cred['password']):
        return errors.response(f'{BP_ID}{func_id}1')
    
    return jsonify({'id': user.id, 'username': user.username, 'password': user.password}), 200
