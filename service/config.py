# -*- coding: utf-8 -*-

DEBUG = True
SECRET_KEY = 'change me please'

SQLALCHEMY_DATABASE_URI = 'sqlite:///users.db'

USERS_ENDPOINT = 'localhost:5001'
STORIES_ENDPOINT = 'localhost:5002'
REACTIONS_ENDPOINT = 'localhost:5003'
SEARCH_ENDPOINT = 'localhost:5004'
AUTH_ENDPOINT = 'localhost:5005'

# Celery
BROKER_TRANSPORT = 'redis'
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_TASK_SERIALIZER = 'json'
CELERY_DISABLE_RATE_LIMITS = True
CELERY_ACCEPT_CONTENT = ['json']

# JWT
SECRET_KEY = 'some-secret-string-CHANGE-ME'
JWT_SECRET_KEY = 'jwt-secret-string-CHANGE-ME'
JWT_TOKEN_LOCATION = ['cookies']
JWT_ACCESS_COOKIE_PATH = '/'
JWT_REFRESH_COOKIE_PATH = '/auth/token_refresh'
JWT_COOKIE_CSRF_PROTECT = True
JWT_COOKIE_SECURE = False  # True for only https
