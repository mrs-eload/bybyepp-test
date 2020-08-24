import json
import logging
import random
from typing import Optional, List
from app.models.Ligand import Ligand
from app.core.config import settings
from pydantic import BaseModel, AnyHttpUrl, Field
from fastapi.encoders import jsonable_encoder

logger = logging.getLogger("uvicorn")

class Structure (BaseModel):
    id: Optional[int]
    name: str = ""
    external_code: str = ""
    biomol_code: Optional[str] = ""
    pdb_file: Optional[str] = ""
    ligands: Optional[List[Ligand]]  = []

    @staticmethod
    def parse_result(result):
        if result is None:
            return result
        logger.info(type(result))
        if type(result) is dict:
            logger.info("THIS IS A DICT")
            structures = []
            for key in result:
                structure = Structure()
                structure = Structure.__from_json(result[key], structure)
                structures.append(structure)

            return structures
        else:
            structure = Structure()
            structure = Structure.__from_json(result, structure)
            logger.info(type(structure))
            logger.info(structure)
            return structure

    @staticmethod
    def __from_json(serial, structure):
        try:
            parsed = json.loads(serial)
            for key in parsed:
                setattr(structure, key, parsed[key])
            return structure
        except json.JSONDecodeError as e:
            logger.error(e)