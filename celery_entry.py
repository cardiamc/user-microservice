# -*- coding: utf-8 -*-
from service import create_app, create_celery
from service.tasks import send_digest

app = create_app(config='service/config.py')
celery = create_celery(app)

POLLING_RATE = 2

#starts periodic email digest
@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(POLLING_RATE, send_digest.s(), name='email-digest')

celery.start()

