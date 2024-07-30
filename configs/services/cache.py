import os

from App.helpers import env
from config import CACHE_PATH, STATIC_APP_NAME

__CONFIG__ = {
    # Driver for cache accessible
    #: BUILD_TYPE:server
    # Drivers: file, memory, redis
    #: END:BUILD_TYPE:server
    #: BUILD_TYPE:!server
    # Drivers: file, memory
    #: END:BUILD_TYPE:!server
    "default": env("CACHE_DRIVER", "file"),

    "drivers": {
        "file": {
            # Path of cache storage
            "path": os.path.join(CACHE_PATH, "storage.cache"),
        },
        #: BUILD_TYPE:server
        "redis": {
            "host": env("REDIS_HOST", "localhost"),
            "port": env("REDIS_PORT", 6379),
            "password": env("REDIS_PASSWORD"),
        },
        #: END:BUILD_TYPE:server
    },

    # Prefix for database based cache services
    "prefix": env("CACHE_PREFIX", STATIC_APP_NAME).replace("-", "_") + "_cache_",
}
