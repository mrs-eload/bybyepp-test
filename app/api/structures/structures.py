import logging
import random
from typing import Optional, List
from fastapi import APIRouter, HTTPException, Body, Response
from app.core.config import settings
from app.models.Structure import Structure
from app.services.RedisService import redis_service

logger = logging.getLogger('3decision.api.structures')
router = APIRouter()

@router.get("/", response_model=list)
def read_structures(q: Optional[str] = None):
    db = redis_service.get_connection(settings.REDIS_DB)
    result = db.hgetall('structures')
    return Structure.parse_result(result)


@router.post("/", response_model=Structure)
def read_structure(structure: Structure = Body(...), q: Optional[str] = None):
    db = redis_service.get_connection(settings.REDIS_DB)
    result = db.hget('structures', structure.external_code)
    result = Structure.parse_result(result)
    if result is not None: raise HTTPException(303, '/structures/' + result.external_code)
    structure.id = random.randint(1, 100000)
    db.hmset('structures', {structure.external_code: structure.json()})
    return structure


@router.get("/{external_code}", response_model=Structure)
def read_structure(external_code: str, q: Optional[str] = None):
    db = redis_service.get_connection(settings.REDIS_DB)
    result = db.hget('structures', external_code)
    result = Structure.parse_result(result)
    if result is None: raise HTTPException(404)
    return result

@router.delete("/{external_code}", response_model=dict)
def read_structure(external_code: str, q: Optional[str] = None):
    db = redis_service.get_connection(settings.REDIS_DB)
    result = db.hget('structures', external_code)
    if result is None: raise HTTPException(404)

    db.hdel('structures', external_code)
    return Response(status_code=204)


@router.put("/{external_code}", response_model=Structure)
def read_structure(external_code: str, item: Structure = Body(...), q: Optional[str] = None):
    if (item.external_code is not None and item.external_code != '') and external_code != item.external_code:
        raise HTTPException(400, "Request parameter doesn't match external code from Body")

    item.external_code = external_code
    db = redis_service.get_connection(settings.REDIS_DB)

    structure = db.hget('structures', external_code)
    structure = Structure.parse_result(structure)

    logger.info('From DB %s', structure)
    logger.info('JSON %s', structure.json())

    if structure is None:
        return None

    structure_dict = item.dict()
    for key in structure_dict:
        if key == 'id' or key == 'external_code': continue
        setattr(structure, key, structure_dict[key])

    json_data = {structure.external_code: structure.json()}
    db.hmset('structures', json_data)

    return structure