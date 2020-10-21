import logging
import json, os, shutil
import random
from time import sleep
from typing import Optional, List
from fastapi import APIRouter, HTTPException, Body, Response, WebSocket, Depends, Cookie, Query, UploadFile, File, Path
from fastapi.responses import JSONResponse
from starlette import status
from starlette.websockets import WebSocketDisconnect

from app.core.config import settings
from app.models.Structure import Structure
from app.services.RedisService import redis_service
from app.workers import tasks


logger = logging.getLogger(__name__)
router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()

@router.get("/", response_model=list)
def read_structures(q: Optional[str] = None):
    db = redis_service.get_connection(settings.REDIS_DB)
    result = db.hgetall('structures')
    return Structure.parse_result(result)


@router.post("/import")
def import_structure(file: UploadFile = File(...)):
    destination = os.path.join(settings.PROJECT_PATH, 'saves', file.filename)
    try:
        logger.info(file.filename)
        with open(destination, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    finally:
        file.file.close()

    res = tasks.launch_remote_process.delay()
    result = res.get()
    logger.info(result)
    return "OK"

# Will register a new structure
# @param is_async : True will return a job id (celery task number), False will wait for the job to finish and send the results
# Async job results retrieval is not done yet
@router.post("/")
def read_structure(structure: Structure = Body(...), is_async: Optional[bool] = False):
    res = tasks.launch_remote_process.delay(structure.external_code, structure.json())
    logger.info('JOB ID %s', res.id)
    return "Itsokay"
    # res = tasks.register_structure.delay(structure.external_code, structure.json())
    # if is_async:
    #     return res.id
    # else:
    #     result = res.get()
    #     return JSONResponse(content=json.dumps(result), status_code=result['details']['code'] )

@router.websocket("/ws/get")
async def websocket_endpoint(websocket: WebSocket):

    await websocket.accept()
    while True:
        try:
            data = await websocket.receive_text()
            db = redis_service.get_connection(settings.REDIS_DB)
            result = db.hget('structures', data)
            result = Structure.parse_result(result)
            logger.info(data)
            logger.info(type(data))
            await websocket.send_json(result.dict())
        except json.JSONDecodeError:
            await websocket.send_json({"data": "error"})

@router.websocket("/ws/getall")
async def websocket_endpoint(websocket: WebSocket):

    db = redis_service.get_connection(settings.REDIS_DB)
    result = db.hgetall('structures')
    result = Structure.parse_result(result)

    await websocket.accept()
    while True:
        try:
            data = await websocket.receive_json()
            logger.info(data)
            logger.info(type(data))
            for val in result:
                await websocket.send_json(val.dict())
        except json.JSONDecodeError:
            await websocket.send_json({"data": "error"})



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