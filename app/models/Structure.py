import json
import logging
import random
from typing import Optional, List
from app.models.Ligand import Ligand
from app.core.config import settings
from app.services.RedisService import redis_service
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
    #
    # @staticmethod
    # def find(external_code) -> bytes or None:
    #     db = redis_service.get_connection(settings.REDIS_DB)
    #     result = db.hget('structures', external_code)
    #     return Structure.__parse_result(result)
    #
    # @staticmethod
    # def get_all():
    #     db = redis_service.get_connection(settings.REDIS_DB)
    #     results = db.hgetall('structures')
    #     return Structure.__parse_result(results)
    #
    # @staticmethod
    # def __parse_result(result):
    #     if result is None:
    #         return result
    #     logger.info(type(result))
    #     if type(result) is dict:
    #         structures = []
    #         for key in result:
    #             structure = Structure()
    #             structure = Structure.__from_json(result[key], structure)
    #             structures.append(structure)
    #
    #         return structures
    #     else:
    #         structure = Structure()
    #         structure = Structure.__from_json(result, structure)
    #         return structure
    #
    # @staticmethod
    # def update(item):
    #     db = redis_service.get_connection(settings.REDIS_DB)
    #
    #     structure = Structure.find(item.external_code)
    #     logger.info('From DB %s', structure)
    #     logger.info('JSON %s', structure.json())
    #     if structure is None:
    #         return None
    #
    #     structure_dict = item.dict()
    #     for key in structure_dict:
    #         if key == 'id' or key == 'external_code': continue
    #         setattr(structure, key, structure_dict[key])
    #
    #     json_data = {structure.external_code: structure.json()}
    #     db.hmset('structures', json_data)
    #
    #     return structure
    #
    # def save(self):
    #     logger.info('Saving %s', self.external_code)
    #     db = redis_service.get_connection(settings.REDIS_DB)
    #     json_data = {self.external_code: self.json()}
    #     db.hmset('structures', json_data)
    #     return self
    #
    # @staticmethod
    # def __from_json(serial, structure):
    #     try:
    #         parsed = json.loads(serial)
    #         for key in parsed:
    #             setattr(structure, key, parsed[key])
    #         return structure
    #     except json.JSONDecodeError as e:
    #         logger.error(e)