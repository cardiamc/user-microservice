import functools

from flask import jsonify, request

'''
Constant value representing the endpoint. This has to be written with two
uppercase letter, eg. API Gateway -> AG)
'''
EP_CODE = 'US'

'''
Dictionary with all errors related to this service and the
corresponding error messages and status_code
'''
EP_DICT = {
    # users.py
    # Get user
    '011': (404, 'User with the requested id does not exist'),

    # Signup
    '021': (400, 'Too many parameters.'),
    '022': (400, 'E-mail, username and password are required'),
    '023': (400, 'Username must be between 5 and 25 characters and must contain only letters and numbers'),
    '024': (400, 'Invalid e-mail address'),
    '025': (400, 'Password must be between 8 and 64 characters'),
    '026': (400, 'First name must be at max 64 characters'),
    '027': (400, 'Last name must be at max 64 characters'),
    '028': (400, 'Invalid parameter (accepted parameters: [username, email, password, firstname, lastname, dateofbirth])'),
    '029': (500, 'An error has occurred during the registration. Try again later.'),

    # Follow
    '031': (400, 'You cannot follow yourself'),
    '032': (404, 'User with the requested id does not exist'),
    '033': (500, 'An error has occurred during the operation.'),

    # Unfollow
    '041': (400, 'You cannot unfollow yourself'),
    '042': (404, 'User with the requested id does not exist'),
    '043': (500, 'An error has occurred during the operation.'),

    # telebot.py
    # Bot register
    '101': (400, 'Username and telegram chat id are required for this operation'),
    '102': (404, 'User with the requested username does not exist'),

    # auth.py
    # Login
    '201': (400, 'Wrong username or password')
}


def response(code):
    '''
    Standard for the error response.

    The code must be written as a three number code, call it xyz, as follows:
        x -> the number of the current blueprint
        y -> the number of the route of the current blueprint
        z -> the number of the error within the current route

    Returns:
        A json response ready to be sent via a Flask view
    '''
    status_code, message = EP_DICT[code]
    return jsonify({
        'code': f'E{EP_CODE}{code}',
        'message': message
    }), status_code
