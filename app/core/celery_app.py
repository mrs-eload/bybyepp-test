from celery import Celery
from app.core.config import settings
import logging
logger = logging.getLogger('[Celery]')
celery_app = Celery("app.services.tasks", broker="amqp://guest:guest@local.discngine.com:5672//", backend="redis://localhost/1")