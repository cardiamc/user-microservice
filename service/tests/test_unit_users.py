import json
import datetime as dt
from service.models import User

MOCK_TOKEN_IDENTITY = {'id': 1,
                       'username': 'test1', 'password': 'test1123'}

class TestAllUsers:

    def test_all_users_success(self, app, client, users, database, jwt_token):
        users.client = client
        
        token = jwt_token.create_token(MOCK_TOKEN_IDENTITY)

        reply = users.all_users(token)
        assert reply.status_code == 200
        
        all_users = [u.to_dict() for u in database.session.query(User).all()]
        all_users = {'users': all_users}
        assert reply.json == all_users

    def test_all_users_no_token(self, app, client, users, database, jwt_token):
        users.client = client

        reply = users.all_users(None)
        assert reply.status_code == 401


class TestGetUser:

    def test_get_user_success(self, app, client, users, database, jwt_token):
        users.client = client
        
        token = jwt_token.create_token(MOCK_TOKEN_IDENTITY)

        reply = users.get_user(token, 2)
        assert reply.status_code == 200

        get_user_res = User.query.get(2).to_dict()
        assert reply.json['user'] == get_user_res
    
    def test_get_user_no_user(self, app, client, users, database, jwt_token):
        users.client = client

        token = jwt_token.create_token(MOCK_TOKEN_IDENTITY)

        reply = users.get_user(token, 180)
        assert reply.status_code == 404
        assert reply.json['code'] == 'EUS011'

    def test_get_user_no_token(self, app, client, users, database, jwt_token):
        users.client = client

        reply = users.get_user(None, 2)
        assert reply.status_code == 401

class TestSignup:

    def test_signup_success(self, app, client, users, database):
        users.client = client

        data = {
            'username': 'test4',
            'email': 'test4@example.com',
            'password': 'test4123',
            'firstname': 'First4',
            'lastname': 'Last4',
            'dateofbirth': '2020-10-5'
        }
        
        reply = users.signup(data)
        assert reply.status_code == 200
    
    def test_signup_toomany_parameters(self, app, client, users, database):
        users.client = client

        data = {
            'username': 'test4',
            'email': 'test4@example.com',
            'password': 'test4123',
            'firstname': 'First4',
            'lastname': 'Last4',
            'dateofbirth': '2020-10-5',
            'toomany?': 'yep, too many'
        }

        reply = users.signup(data)
        assert reply.status_code == 400
        assert reply.json['code'] == 'EUS021'

    def test_signup_username_missing(self, app, client, users, database):
        users.client = client

        data = {
            'email': 'test4@example.com',
            'password': 'test4123',
            'firstname': 'First4',
            'lastname': 'Last4',
            'dateofbirth': '2020-10-5'
        }

        reply = users.signup(data)
        assert reply.status_code == 400
        assert reply.json['code'] == 'EUS022'

    def test_signup_wrong_username(self, app, client, users, database):
        users.client = client

        data = {
            'username': 'te',
            'email': 'test4@example.com',
            'password': 'test4123',
            'firstname': 'First4',
            'lastname': 'Last4',
            'dateofbirth': '2020-10-5'
        }

        reply = users.signup(data)
        assert reply.status_code == 400
        assert reply.json['code'] == 'EUS023'

        data['username'] = 'test4@'

        reply = users.signup(data)
        assert reply.status_code == 400
        assert reply.json['code'] == 'EUS023'
    
    def test_signup_wrong_email(self, app, client, users, database):
        users.client = client

        data = {
            'username': 'test4',
            'email': 'test4example.com',
            'password': 'test4123',
            'firstname': 'First4',
            'lastname': 'Last4',
            'dateofbirth': '2020-10-5'
        }

        reply = users.signup(data)
        assert reply.status_code == 400
        assert reply.json['code'] == 'EUS024'
    
    def test_signup_wrong_password(self, app, client, users, database):
        users.client = client

        data = {
            'username': 'test4',
            'email': 'test4@example.com',
            'password': 'pwd',
            'firstname': 'First4',
            'lastname': 'Last4',
            'dateofbirth': '2020-10-5'
        }

        reply = users.signup(data)
        assert reply.status_code == 400
        assert reply.json['code'] == 'EUS025'
    
    def test_signup_wrong_firstname(self, app, client, users, database):
        users.client = client

        data = {
            'username': 'test4',
            'email': 'test4@example.com',
            'password': 'test4123',
            'firstname': ''.join(['a' for _ in range(65)]),
            'lastname': 'Last4',
            'dateofbirth': '2020-10-5'
        }

        reply = users.signup(data)
        assert reply.status_code == 400
        assert reply.json['code'] == 'EUS026'
    
    def test_signup_wrong_lastname(self, app, client, users, database):
        users.client = client

        data = {
            'username': 'test4',
            'email': 'test4@example.com',
            'password': 'test4123',
            'firstname': 'First4',
            'lastname': ''.join(['a' for _ in range(65)]),
            'dateofbirth': '2020-10-5'
        }

        reply = users.signup(data)
        assert reply.status_code == 400
        assert reply.json['code'] == 'EUS026'
    
    def test_signup_wrong_dateofbirth(self, app, client, users, database):
        users.client = client

        data = {
            'username': 'test4',
            'email': 'test4@example.com',
            'password': 'test4123',
            'firstname': 'First4',
            'lastname': 'Last4',
            'dateofbirth': 'wrongdate'
        }

        reply = users.signup(data)
        assert reply.status_code == 400
        assert reply.json['code'] == 'EUS027'
    
    def test_signup_wrong_param(self, app, client, users, database):
        users.client = client

        data = {
            'username': 'test4',
            'email': 'test4@example.com',
            'password': 'test4123',
            'firstname': 'First4',
            'lastname': 'Last4',
            'wrongparam?': 'Yep, wrong'
        }

        reply = users.signup(data)
        assert reply.status_code == 400
        assert reply.json['code'] == 'EUS028'
    
    def test_signup_username_exists(self, app, client, users, database):
        users.client = client

        data = {
            'username': 'test1',
            'email': 'test5@example.com',
            'password': 'test4123',
            'firstname': 'First4',
            'lastname': 'Last4',
            'dateofbirth': '2020-10-5'
        }

        reply = users.signup(data)
        assert reply.status_code == 409
        assert reply.json['code'] == 'EUS029U'
    
    def test_signup_email_exists(self, app, client, users, database):
        users.client = client

        data = {
            'username': 'test5',
            'email': 'test1@example.com',
            'password': 'test4123',
            'firstname': 'First4',
            'lastname': 'Last4',
            'dateofbirth': '2020-10-5'
        }

        reply = users.signup(data)
        assert reply.status_code == 409
        assert reply.json['code'] == 'EUS029E'


class TestFollow:

    def test_follow_success(self, app, client, users, database, jwt_token):
        users.client = client
        
        token = jwt_token.create_token(MOCK_TOKEN_IDENTITY)

        reply = users.follow(token, 2)
        assert reply.status_code == 200

    def test_follow_myself(self, app, client, users, database, jwt_token):
        users.client = client
        
        token = jwt_token.create_token(MOCK_TOKEN_IDENTITY)

        reply = users.follow(token, 1)
        assert reply.status_code == 400
        assert reply.json['code'] == 'EUS031'
    
    def test_follow_non_existing_user(self, app, client, users, database, jwt_token):
        users.client = client
        
        token = jwt_token.create_token(MOCK_TOKEN_IDENTITY)

        reply = users.follow(token, 180)
        assert reply.status_code == 404
        assert reply.json['code'] == 'EUS032'
    
    def test_follow_already_following(self, app, client, users, database, jwt_token):
        users.client = client
        
        token = jwt_token.create_token(MOCK_TOKEN_IDENTITY)

        users.follow(token, 2)
        reply = users.follow(token, 2)
        assert reply.status_code == 409
        assert reply.json['code'] == 'EUS033'

    def test_follow_no_token(self, app, client, users, database, jwt_token):
        users.client = client

        reply = users.follow(None, 2)
        assert reply.status_code == 401


class TestUnfollow:

    def test_unfollow_success(self, app, client, users, database, jwt_token):
        users.client = client
        
        token = jwt_token.create_token(MOCK_TOKEN_IDENTITY)
        users.follow(token, 2)
        reply = users.unfollow(token, 2)
        assert reply.status_code == 200

    def test_unfollow_myself(self, app, client, users, database, jwt_token):
        users.client = client
        
        token = jwt_token.create_token(MOCK_TOKEN_IDENTITY)

        reply = users.unfollow(token, 1)
        assert reply.status_code == 400
        assert reply.json['code'] == 'EUS041'

    def test_unfollow_non_existing_user(self, app, client, users, database, jwt_token):
        users.client = client
        
        token = jwt_token.create_token(MOCK_TOKEN_IDENTITY)

        reply = users.unfollow(token, 180)
        assert reply.status_code == 404
        assert reply.json['code'] == 'EUS042'

    def test_follow_not_following_yet(self, app, client, users, database, jwt_token):
        users.client = client
        
        token = jwt_token.create_token(MOCK_TOKEN_IDENTITY)

        reply = users.unfollow(token, 2)
        assert reply.status_code == 409
        assert reply.json['code'] == 'EUS043'

    def test_unfollow_no_token(self, app, client, users, database, jwt_token):
        users.client = client

        reply = users.unfollow(None, 2)
        assert reply.status_code == 401


class TestFollowed:

    def test_followed_success(self, app, client, users, database, jwt_token):
        users.client = client

        token = jwt_token.create_token(MOCK_TOKEN_IDENTITY)
        users.follow(token, 2)

        me = User.query.get(1)
        followed_users = [x.to_dict() for x in me.follows]
        assert followed_users != []

        reply = users.get_followed(token)
        assert reply.status_code == 200
        assert reply.json['followed_users'] == followed_users
    
    def test_followed_no_token(self, app, client, users, database, jwt_token):
        users.client = client

        reply = users.get_followed(None)
        assert reply.status_code == 401
