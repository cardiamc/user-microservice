import telegram
from telegram.ext import CommandHandler, Updater

from service.models import User

TOKEN = '1057812273:AAH0w4miBCIhL-lRV4viJ1-egoA8-rcBrs0'

def create_telebot():
    telegram_bot = telegram.Bot(TOKEN)
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    
    def on_start(update, context):
        chat_id = update.message.chat_id    
        return telegram_bot.send_message(
            chat_id, 
            'Please use /login <username> to receive stories from your followed users'
        )

    def on_login(update, context):
        chat_id = update.effective_chat.id
        username = ' '.join(context.args)
        if username == '':
            telegram_bot.send_message(
                chat_id=chat_id,
                text='Use the command /login <username>'
            )
        
        user = User.query.filter_by(username=username).one_or_none()
        if user is not None:
            user.telegram_chat_id = int(chat_id)
            telegram_bot.send_message(
                chat_id=chat_id,
                text='You will now receive updates about followed users'
            )
        else:
            telegram_bot.send_message(
                chat_id=chat_id, 
                text='No user is registered with this username'
            )

    # Add functions to the dispatcher to be handled.
    dp.add_handler(CommandHandler('start', on_start))
    dp.add_handler(CommandHandler('login', on_login))
    updater.start_polling()
    
    return telegram_bot
