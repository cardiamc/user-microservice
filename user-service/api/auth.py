from flask import Blueprint

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST'])
def login():
    '''
    Process login requests from user via username or email and password.

    Returns:
        200 -> Successful authentication
        300 -> Request has bad syntax
        403 -> Provided data is invalid
    '''
    pass


@auth.route('/logout', methods=['POST'])
def logout():
    '''
    Process logout requests from user already logged via bearer token.

    Returns:
        200 -> User was authenticated and it is not anymore
        301 -> Authentication token is missing or invalid
    '''
    pass


@auth.route('/signup', methods=['POST'])
def signup():
    '''
    Process signup request from users in JSON format.

    Returns:
        200 -> Successful registration
        400 -> Bad request body syntax or validation error
    '''
    pass
