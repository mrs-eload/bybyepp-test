import os, sys
import logging
import uvicorn
from fastapi import FastAPI

from app.api import api
from app.core.config import settings
from app.services.RedisService import redis_service

main_logger= logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.INFO)


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

#If running in IDE spawn own uvicorn server instance
if os.getenv('IDE') is not None:
    if __name__ == "__main__":
        uvicorn.run(app, host="0.0.0.0", port=8000, use_colors=True)