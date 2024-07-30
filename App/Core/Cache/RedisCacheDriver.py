from App.Core.Abstract import AbstractCacheDriver
from App.Core import Config

from typing import Any

import redis


class RedisCacheDriver(AbstractCacheDriver):
    def __init__(self, config: Config):
        cache_data = config.get('cache')
        config = cache_data['drivers']['redis']

        self.__connection = redis.Redis(config['host'], config['port'], password=config['password'])

        self.__prefix = cache_data['prefix']

    def get(self, key: str) -> Any:
        return self.__connection.get(self.__prefix + key)

    def set(self, key: str, value: Any):
        self.__connection.set(self.__prefix + key, value)

    def clear(self):
        self.__connection.delete(*self.__connection.keys(f"{self.__prefix}:"))
