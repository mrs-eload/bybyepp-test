from raven import Client
import random

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

#Start a celery task, at this point everything must be serialized and out of context
@celery_app.task(acks_late=True)
def register_structure(external_code: str, structure: str) -> str:
    logger.info('Starting task structure registration')
    res = __save(external_code=external_code, i_structure=structure)
    logger.info('Finish structure registration')
    return res


#Save and send back results
def __save(external_code, i_structure):
    db = redis_service.connect(settings.REDIS_DB)
    result = db.hget('structures', external_code)
    result = Structure.parse_result(result)
    structure = Structure.parse_result(i_structure)
    if result is not None: return {'status': 'error', 'details' : {'code': 303, 'url': '/structures/' + result.external_code}}
    structure.id = random.randint(1, 100000)
    db.hmset('structures', {structure.external_code: structure.json()})
    return {'status': 'success', 'details': {'code': 200, 'structure': i_structure}}