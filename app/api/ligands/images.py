import logging
import random
from typing import Optional
from fastapi import APIRouter, HTTPException, Body

logger = logging.getLogger('3decision.api.ligandsimages')

router = APIRouter()