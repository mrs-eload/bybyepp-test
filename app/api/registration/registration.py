import logging
import random
from typing import Optional
from fastapi import APIRouter, HTTPException, Body

logger = logging.getLogger('api.registration')
router = APIRouter()