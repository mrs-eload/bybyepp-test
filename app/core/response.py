import json
from fastapi import APIRouter, HTTPException, Body, Response

class Responsed(Response):
    def __init__(self, to_send):
        super()
        self.status_code = to_send['details']['code']
        self.content = json.dumps(to_send)

