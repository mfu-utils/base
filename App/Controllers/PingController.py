from config import VERSION_DETAILED, VERSION_SHOW
from App.helpers import config


class PingController:
    # noinspection PyMethodMayBeStatic
    def invoke(self):
        return {
            'name': config('app.name'),
            'version_show': VERSION_SHOW,
            'version_detailed': VERSION_DETAILED,
        }
