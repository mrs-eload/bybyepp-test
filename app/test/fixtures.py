import sys
import json
import random
import logging

from app.models.Structure import Structure
from app.models.Ligand import Ligand

from app.services.RedisService import redis_service

logger = logging.getLogger("uvicorn")

def load_fixtures():

    logger.info("Loading structures fixtures ...")
    codes = ["5dls", "1uyd", "2po6", "4bdj"]
    redis = redis_service.connect("3decision_data",0)
    json_data = {}
    json_data['structures'] = {}

    for code in  codes:
        logger.info(("Saving into redis", code))
        structure = Structure()
        structure.id = random.randint(1,100000)
        structure.name = code + ' structure'
        structure.external_code = code
        json_data['structures'][code] = structure.json()

    redis.hmset('structures', json_data['structures'])
    logger.info(type(json_data))
    logger.info(json_data)
