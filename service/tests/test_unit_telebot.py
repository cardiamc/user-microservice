import json

class TestTelebot:

    def test_register_bot_success(self, app, client, telebot, database):
        telebot.client = client

        reply = telebot.register('test1', 1234)
        assert reply.status_code == 200
    
    def test_register_bot_username_missing(self, app, client, telebot, database):
        telebot.client = client

        reply = telebot.register('test1', None)
        assert reply.status_code == 400
        assert reply.json['code'] == 'EUS101'

    def test_register_bot_chat_id_missing(self, app, client, telebot, database):
        telebot.client = client

        reply = telebot.register(None, 1234)
        assert reply.status_code == 400
        assert reply.json['code'] == 'EUS101'
    
    def register_bot_invalid_user(self, app, client, telebot, database):
        telebot.client = client

        reply = telebot.register('wrong_user', 1234)
        assert reply.status_code == 404
        assert reply.json['code'] == 'EUS102'
