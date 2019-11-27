# -*- coding: utf-8 -*-

from celery import Celery
celery = Celery()

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

#from service.utility.telebot_utils import create_telebot
#telebot = create_telebot()

from ptbtest import Mockbot
mockbot = Mockbot()