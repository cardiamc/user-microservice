from flask import Blueprint, jsonify, request
import flask_jwt_extended as jwt

from service.models import db, User
from sqlalchemy.exc import IntegrityError

import re

from service.utility import errors

users = Blueprint('users', __name__)

BP_ID = 0

@users.route('/users', methods=['GET'])
@jwt.jwt_required
def users_(func_id=0):
    '''
    Provides the list of all the users.

    Returns:
        200 -> the list has been provided successfully
    '''
    users = User.query.all()

    return jsonify({'users': [u.to_dict() for u in users]}), 200


@users.route('/users/<user_id>', methods=['GET'])
@jwt.jwt_required
def get_user(user_id, func_id=1):
    '''
    Opens the wall of the user with id <user_id>.

    Returns:
        200 -> the user's wall with the list of all his/her posted stories
    '''
    
    user = User.query.get(user_id).to_dict()
    if user is None:
        return errors.response(f'{BP_ID}{func_id}1')
    
    return jsonify({'user': user}), 200


@users.route('/signup', methods=['POST'])
def signup(func_id=2):
    '''
    Registers a user.

    Returns:
        200 -> the user has been registered successfully
    '''

    params = request.get_json()

    if len(params) > 6:
        return errors.response(f'{BP_ID}{func_id}1')

    if not all(x in params for x in ['email', 'username', 'password']):
        return errors.response(f'{BP_ID}{func_id}2')

    new_user = User()

    err_code = None
    for k in params:
        if k == 'username':
            username = params[k]
            if 5 <= len(username) <= 25 and re.search(r'^\w+$', username):
                new_user.username = username
            else:
                err_code = 3
                break
            
        elif k == 'email':
            email = params[k]
            if re.search(r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$', email):
                new_user.email = email
            else:
                err_code = 4
                break

        elif k == 'password':
            password = params[k]
            if 8 <= len(password) <= 64:
                new_user.set_password(password)
            else:
                err_code = 5
                break

        elif k == 'firstname':
            firstname = params[k]
            if len(firstname) <= 64:
                new_user.firstname = firstname
            else:
                err_code = 6
                break

        elif k == 'lastname':
            lastname = params[k]
            if len(lastname) <= 64:
                new_user.lastname = lastname
            else:
                err_code = 6
                break

        elif k == 'dateofbirth':
            new_user.dateofbirth = params[k]
        
        else:
            err_code = 7
            break

    if err_code is not None:
        return errors.response(f'{BP_ID}{func_id}{err_code}')
    
    db.session.add(new_user)
    try:
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        if 'user.username' in str(e):
            return errors.response(f'{BP_ID}{func_id}8')
        if 'user.email' in str(e):
            return errors.response(f'{BP_ID}{func_id}9')

    return jsonify({}), 200


@users.route('/users/<user_id>/follow', methods=['POST'])
@jwt.jwt_required
def follow(user_id, func_id=3):
    '''
    Follows the user with id <user_id>. 

    Returns:
        200 -> user followed successfully
    '''
    follower = jwt.get_jwt_identity()['id']
    followee = int(user_id)
    if follower == followee:
        return errors.response(f'{BP_ID}{func_id}1')

    followee = User.query.get(followee)
    if followee is None:
        return errors.response(f'{BP_ID}{func_id}2')
    
    follower = User.query.get(follower)
    follower.follows.append(followee)

    try:
        db.session.commit()
    except IntegrityError:
        return errors.response(f'{BP_ID}{func_id}3')

    return jsonify({}), 200


@users.route('/users/<user_id>/follow', methods=['DELETE'])
@jwt.jwt_required
def unfollow(user_id, func_id=4):
    '''
    Unfollows the user with id <user_id>. 

    Returns:
        200 -> user unfollowed successfully
    '''
    follower = jwt.get_jwt_identity()['id']
    followee = int(user_id)
    if follower == followee:
        return errors.response(f'{BP_ID}{func_id}1')

    followee = User.query.get(followee)
    if followee is None:
        return errors.response(f'{BP_ID}{func_id}2')
    
    follower = User.query.get(follower)
    follower.follows.remove(followee)

    try:
        db.session.commit()
    except IntegrityError:
        return errors.response(f'{BP_ID}{func_id}3')

    return jsonify({}), 200


@users.route('/followed', methods=['GET'])
@jwt.jwt_required
def get_followed(func_id=5):
    '''
    Gets the list of the current user's followers.

    Returns:
        200 -> the list has been returned correctly
    '''
    me = User.query.get(jwt.get_jwt_identity()['id'])
    users = [x.to_dict() for x in me.follows]
    return jsonify({'users': users}), 200
