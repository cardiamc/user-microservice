import os
import tempfile
import datetime

import json
import pytest

import flask_jwt_extended as jwt
from service.models import User, db
from service.app import create_app


@pytest.fixture(scope='class')
def app():
    db_fd, db_path = tempfile.mkstemp()
    db_url = 'sqlite:///' + db_path
    app = create_app(config='tests/config_test.py', database=db_url)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture(scope='class')
def client_factory(app):

    class ClientFactory:

        def __init__(self, app):
            self._app = app

        def get(self):
            return self._app.test_client()

    return ClientFactory(app)


@pytest.fixture(scope='class')
def client(app, client_factory):
    return client_factory.get()


def _init_database(db):
    '''
    Initializes the database for testing.
    '''
    example1 = User()
    example1.username = 'test1'
    example1.firstname = 'First1'
    example1.lastname = 'Last1'
    example1.email = 'test1@example.com'
    example1.dateofbirth = datetime.datetime(2020, 10, 5)
    example1.is_admin = False
    example1.set_password('test1123')
    db.session.add(example1)

    example2 = User()
    example2.username = 'test2'
    example2.firstname = 'First2'
    example2.lastname = 'Last2'
    example2.email = 'test2@example.com'
    example2.dateofbirth = datetime.datetime(2020, 10, 5)
    example2.is_admin = False
    example2.set_password('test2123')
    db.session.add(example2)

    example3 = User()
    example3.username = 'test3'
    example3.firstname = 'First3'
    example3.lastname = 'Last3'
    example3.email = 'test3@example.com'
    example3.dateofbirth = datetime.datetime(2020, 10, 5)
    example3.is_admin = False
    example3.set_password('test3123')
    db.session.add(example3)

    db.session.commit()


@pytest.fixture
def database(app):
    '''
    Provides a reference to the temporary database in the app context. Use
    this instance instead of importing db from monolith.db.
    '''
    with app.app_context():
        db.create_all()

        _init_database(db)
        yield db

        db.drop_all()
        db.session.commit()


@pytest.fixture('class')
def jwt_token(app):

    class JWTActions():

        def create_token(self, identity, refresh=False, max_age=None):
            with app.app_context():
                if refresh:
                    return jwt.create_refresh_token(identity,
                                                    expires_delta=max_age)
                return jwt.create_access_token(identity,
                                               expires_delta=max_age)

        def set_token(self, response, token, refresh=False):
            with app.app_context():
                if refresh:
                    jwt.set_refresh_cookies(response, token)
                else:
                    jwt.set_access_cookies(response, token)

        def token_headers(self, identity, refresh=False, max_age=None):
            with app.app_context():
                token = self.create_token(identity, max_age=max_age)
                res = jsonify({})
                self.set_token(res, token)
                if refresh:
                    token = self.create_token(
                        identity, refresh=True, max_age=max_age)
                    self.set_token(res, token, refresh=True)
                return res.headers['Set-Cookie']

    return JWTActions()


@pytest.fixture(scope='class')
def users():

    class UsersActions:

        def __init__(self):
            self.client = None

        def get_users(self):
            assert self.client is not None
            return self.client.get(
                '/users'
            )
        
        def get_user(self, user_id):
            assert self.client is not None
            return self.client.get(
                f'/users/{user_id}'
            )
        
        def signup(self, data):
            assert self.client is not None
            return self.client.post(
                '/signup',
                data=json.dumps(data),
                content_type='application/json')
        
        def follow(self, user_id):
            assert self.client is not None
            return self.client.post(
                f'/users/{user_id}/follow'
            )
        
        def unfollow(self, user_id):
            assert self.client is not None
            return self.client.delete(
                f'/users/{user_id}/follow'
            )

        def get_followed(self):
            assert self.client is not None
            return self.client.get(
                '/followed'
            )
        
    return UsersActions()


@pytest.fixture(scope='class')
def telebot():

    class TelebotActions:

        def __init__(self):
            self.client = None

        def register(self, username, chat_id):
            assert self.client is not None
            qstring = '?'
            if username is not None:
                qstring = f'{qstring}username={username}&'
            if chat_id is not None:
                qstring = f'{qstring}chat_id={chat_id}&'

            return self.client.post(
                f'/bot/register{qstring[:-1]}'
            )
    return TelebotActions()


@pytest.fixture(scope='class')
def auth():

    class AuthActions:

        def __init__(self):
            self.client = None

        def login(self, data):
            assert self.client is not None
            return self.client.post(
                '/login',
                json=json.dumps(data)
            )

    return AuthActions()