from raven import Client
import json
import random
from time import sleep

from app.core.celery_app import celery_app
from app.core.config import settings
from celery.utils.log import get_task_logger
from app.models.Structure import Structure
from app.services.RedisService import redis_service

logger = get_task_logger(__name__)
client_sentry = Client(settings.SENTRY_DSN)


@celery_app.task
def test_celery(word: str) -> str:
    return f"test task return {word}"


@celery_app.task(acks_late=True)
def register_structure(external_code: str, structure: str) -> str:
    logger.info('Starting task structure registration')
    res = save(external_code=external_code, structure=structure)
    logger.info('Finish structure registration')
    return res

def save(external_code, structure):
    db = redis_service.connect(settings.REDIS_DB)
    result = db.hget('structures', external_code)
    result = Structure.parse_result(result)
    struc = Structure.parse_result(structure)
    if result is not None: return {'status': 'error', 'details' : {'code': 303, 'url': '/structures/' + result.external_code}}
    struc.id = random.randint(1, 100000)
    db.hmset('structures', {struc.external_code: struc.json()})
    return {'status': 'success', 'details': {'code': 200, 'structure': structure}}