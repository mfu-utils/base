from App.Core import Config
from App.Core.Cache import CacheManager
from App.Core.Console import Output
from App.Core.Logger import Log
from App.Services.PrinterService import PrinterService


class PrintersController:
    # noinspection PyMethodMayBeStatic
    def list(self, parameters: dict, log: Log, config: Config, cache: CacheManager, console: Output):
        service = PrinterService(cache, log, config, console)

        if parameters.get('update-cache') or (not config.get('printing.use_cached_devices')):
            service.update_printers_cache()

        return service.get_printers()

    # noinspection PyMethodMayBeStatic
    def use_cache(self, config: Config):
        return config.get('printing.use_cached_devices')
