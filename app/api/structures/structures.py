import logging
import random
from typing import Optional
from fastapi import APIRouter, HTTPException, Body
from app.models.Structure import Structure

logger = logging.getLogger('3decision.api.structures')
router = APIRouter()

@router.get("/")
def read_root():
    return {"Hello": "World"}

@router.get("/structures", response_model=list)
def read_structure(q: Optional[str] = None):
    items =  Structure.get_all()
    if items is None: return []
    return items


@router.get("/structures/{external_code}", response_model=Structure)
def read_structure(external_code: str, q: Optional[str] = None):
    item = Structure.find(external_code)
    if item is None: raise HTTPException(404)
    return item


@router.post("/structures", response_model=Structure)
def read_structure(item: Structure = Body(...), q: Optional[str] = None):
    result = Structure.find(item.external_code)
    if result is not None: raise HTTPException(302, result.json())
    item.id = random.randint(1, 100000)
    new_structure = item.save()
    return new_structure


@router.put("/structures/{external_code}", response_model=Structure)
def read_structure(external_code: str, item: Structure = Body(...), q: Optional[str] = None):
    logger.info(external_code)
    logger.info(item)
    logger.info(item.external_code)

    if (item.external_code is not None and item.external_code != '') and external_code != item.external_code:
        logger.error('Raising 400')
        raise HTTPException(400)

    item.external_code = external_code
    saved_item = Structure.update(item)
    return saved_item