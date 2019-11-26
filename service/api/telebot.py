from flask import Blueprint, request, jsonify
from service.models import db, User

from service.utility import errors

telebot = Blueprint('telebot', __name__)

BP_ID = 1

@telebot.route('/bot/register', methods=['POST'])
def bot_register(func_id=0):
    username = request.args.get('username')
    chat_id = request.args.get('chat_id')

    if username is None or chat_id is None:
        return errors.response(f'{BP_ID}{func_id}1')

    user = User.query.filter_by(username=username).one_or_none()
    if user is not None:
        user.telegram_chat_id = chat_id
        db.session.commit()
        return jsonify({}), 200

    return errors.response(f'{BP_ID}{func_id}2')

