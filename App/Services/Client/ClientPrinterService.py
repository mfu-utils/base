from typing import Optional

from App.Core import Filesystem
from App.Core.Network.Client import ClientConfig
from App.Core.Network.Protocol.Responses.AbstractResponse import AbstractResponse
from App.DTO.Client import PrintingDocumentDTO
from App.Services import PrinterService
from App.helpers import cache, logger, config, console, network_manager


class ClientPrinterService(PrinterService):
    def __init__(self):
        super(ClientPrinterService, self).__init__(cache(), logger(), config(), console())

        self._network_manager = network_manager()

    def on_success_print(self, device: str, path: str, response: AbstractResponse):
        self._logger.success(f"Success send to response ({device}). {response.data()}")

    def on_error_print(self, device: str, path: str, message: Optional[str]):
        self._logger.error(f"Cannot send to printing ({device}). {message or ''}")

    def send_to_print(self, printing_doc: PrintingDocumentDTO, count_pages: int, path: str):
        printing_doc.file = Filesystem.read_file(path, True)

        (
            super(ClientPrinterService, self)
            .send_to_print_one(self._network_manager, printing_doc, count_pages, ClientConfig.client_ui())
            .then(lambda x: self.on_success_print(printing_doc.device, path, x))
            .catch(lambda x: self.on_error_print(printing_doc.device, path, x))
        )
