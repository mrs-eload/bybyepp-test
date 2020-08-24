import redis
import logging
from app.helpers.Singleton import Singleton

logger = logging.getLogger("redis")

class RedisService(metaclass=Singleton):

    def __init__(self):
        self.__connections = {}

    # Get existing Redis connection
    def get_connection(self, name: str) -> redis.Redis:
        return self.__connections.get(name)

    # Create new connection to a Redis database
    def connect(self, name=None, db=0, host="127.0.0.1", port=6379):
        logger.debug('Trying to connect to Redis using %s', (host + ':' + str(port) + ' db:' + str(db)))

        connection_string = name if name is not None else (host+"::"+str(port)+"::"+str(db))
        logger.debug('Connection string %s', connection_string)

        r = self.__connections.get(connection_string)
        if r is None:
            r = redis.Redis(host, port, db, charset="utf-8")

        max_retry = 5
        retry = 0

        def try_connect(cls):
            try:
                r.ping()
                logger.debug('Redis reachable')
                cls.__connections[connection_string] = r
                return True
            except redis.RedisError as e:
                return e

        while retry < max_retry:
            con = try_connect(self)
            if con is not True:
                logger.debug('Connection attempt %s', retry)
                retry = retry + 1
            else:
                break
        if retry <= max_retry:
            return r
        else:
            logger.critical('Fail to connect to Redis')
            logger.exception('Can\'t connect to Redis using %s', (host + ':' + str(port) + ' db:' + str(db)))

    @staticmethod
    def server() -> redis:
        return redis

    def to_dict(self, string):
        string.split(' ')

redis_service = RedisService()