import os, sys
import logging
import logging.config
import string
import time

import uvicorn
import random
from fastapi import FastAPI, Request

import app.workers.tasks as tasks
from app.api import api
from app.core.config import settings
from app.services.RedisService import redis_service

logging.config.fileConfig('logging.ini', disable_existing_loggers=False)
main_logger= logging.getLogger(__name__)

def create_app() -> FastAPI:
    debug = False
    logger = logging.getLogger("uvicorn")

    #Connect to redis database
    redis_service.connect(settings.REDIS_DB, 0)

    #Configure app to run in debug mode
    if os.getenv('DEV') is not None:
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
        debug = True
        main_logger.setLevel(logging.DEBUG)
        logger.setLevel(logging.DEBUG)
        main_logger.debug('Setting Uvicorn loggin to DEBUG')
        main_logger.debug('Load fixture')

        #Register dummy data to redis
        from app.test.fixtures import load_fixtures
        load_fixtures()

    #Create FastAPI app
    app = FastAPI(title='3decision_backend', debug=debug)
    app.router.include_router(api.api_router)
    app.logger = logger
    return app


#Boostrap application
app = create_app()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    idem = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    main_logger.info(f"rid={idem} start request path={request.url.path}")
    start_time = time.time()

    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000
    formatted_process_time = '{0:.2f}'.format(process_time)
    main_logger.info(f"rid={idem} completed_in={formatted_process_time}ms status_code={response.status_code}")

    return response

#If running in IDE spawn own uvicorn server instance
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5500, use_colors=True)