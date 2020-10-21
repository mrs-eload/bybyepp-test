from celery import Celery
import os
import logging
import app.workers.tasks
logger = logging.getLogger(__name__)

# Bind python to running celery instance
# Broker is Rabbit MQ
# Results are stored in Redis on database 1
celery_app = Celery("app.services.tasks", broker="amqp://guest:guest@local.discngine.com:5672//", backend="redis://localhost/1")
