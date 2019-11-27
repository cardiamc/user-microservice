# -*- coding: utf-8 -*-

from celery import Celery
from flask import Flask

from flask_jwt_extended import JWTManager

from service.extensions import db, celery
from service.api import users, auth
from service.utility.telebot_utils import create_telebot

__all__ = ('create_app', 'create_celery')

# Import blueprints and insert in the list
BLUEPRINTS = (users, auth)


def create_app(config=None, app_name='users-service', blueprints=None, database=None):
    app = Flask(app_name)

    if config:
        app.config.from_pyfile(config)

    if database is not None:
        app.config['SQLALCHEMY_DATABASE_URI'] = database
        
    if blueprints is None:
        blueprints = BLUEPRINTS

    jwt = JWTManager(app)
    create_celery(app)
    build_blueprints(app, blueprints)
    db.init_app(app)
    celery.config_from_object(app.config)
    
    updater = create_telebot()
    app.config['TELEGRAM_UPDATER'] = updater

    try:
        db.create_all(app=app)
    except Exception:
        print("DB already existed")

    return app


def create_celery(app):
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask

    return celery


def build_blueprints(app, blueprints):
    for blueprint in blueprints:
        app.register_blueprint(blueprint)
