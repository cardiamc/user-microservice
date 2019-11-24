import json
from service.models import User

class TestAuth:

    def test_login_success(self, app, client, auth, database):
        auth.client = client

        data = {
            'username': 'test1',
            'password': 'test1123'
        }
        
        reply = auth.login(data)

        user = database.session.query(User).get(1)
        json_reply = {
            'id': 1,
            'username': user.username,
            'password': user.password
        }

        assert reply.status_code == 200
        assert reply.json == json_reply
    
    def test_login_wrong_username(self, app, client, auth, database):
        auth.client = client

        data = {
            'username': 'wrongusr',
            'password': 'test1123'
        }
        
        reply = auth.login(data)

        assert reply.status_code == 400
        assert reply.json['code'] == 'EUS201'
    
    def test_login_wrong_password(self, app, client, auth, database):
        auth.client = client

        data = {
            'username': 'test1',
            'password': 'wrongpwd'
        }
        
        reply = auth.login(data)

        assert reply.status_code == 400
        assert reply.json['code'] == 'EUS201'