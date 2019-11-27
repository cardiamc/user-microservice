import requests
from requests.exceptions import Timeout
from flask import current_app as app

from smtplib import SMTP
from email.message import EmailMessage
from service.models import User

from service.extensions import celery, db#, telebot

import datetime as dt

@celery.task
def send_digest():
    '''
    Send the digest of all the stories written in the last month by the followed users.
    '''
    now = dt.datetime.now().strftime("%Y-%m-%d")
    month = (dt.datetime.now() - dt.timedelta(days=30)).strftime("%Y-%m-%d")
    reply = requests.get(
        f'{app.config["STORIES_ENDPOINT"]}/stories?from={month}'
    )
    
    stories = reply.json()
    stories_by_author = {}
    for s in stories:
        a_id = s['author_id']
        if a_id not in stories_by_author:
            stories_by_author[a_id] = []

        stories_by_author[a_id].append(
            f'Story {s["id"]}: {s["text"]} --- Likes: {s["likes"]}- Dislikes: {s["dislikes"]} - Date: {s["date"]}'
        )

    users = db.session.query(User).all()
    for u in users:
        email = EmailMessage()
        email['Subject'] = f'Storyteller digest for you from {month} to {now}'
        email['From'] = 'digest@localhost'
        email['To'] = u.email
        msg = ''
        for f in u.follows:
            if f in stories_by_author:
                msg += f'Author {f}:\n' + '\n'.join(stories_by_author[f]) + '\n'
        email.set_content(msg)

        with SMTP('localhost', 8025) as smtp:
            smtp.send_message(email)


@celery.task
def task_request_telegram(story):
    users = db.session.query(User).all()
    for u in users:
        if int(story['author_id']) in u.follows:
            text = f'Author {story["author_id"]}: {story["text"]}'
            app.config['TELEGRAM_UPDATER'].bot.send_message(u.telegram_chat_id, text)