# -*- coding: utf-8 -*-

from celery import Celery
celery = Celery()

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from utility.telebot_utils import create_bot
telebot = create_bot()

from ptbtest import Mockbot
mockbot = Mockbot()