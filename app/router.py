import logging
from typing import Optional
from fastapi import HTTPException, Body
from  app.models.Structure import Structure

logger = logging.getLogger('uvicorn')