# -*- coding: utf-8 -*-
from gateway import create_app, create_celery


app = create_app(config='config.py')
celery = create_celery(app)
celery.start()
