from celery import Celery
from app.core.config import settings

celery_app = Celery("worker", broker="amqp://guest@queue//")

celery_app.conf.task_routes = settings.PROCESS_ROUTES