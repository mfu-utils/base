from typing import List, Dict

from PySide6.QtGui import QDragEnterEvent, QDropEvent, QDragLeaveEvent
from PySide6.QtWidgets import QWidget, QPushButton, QLabel
from PySide6.QtCore import QUrl, Qt, Signal

from App.Core.Network.Client import ClientConfig
from App.Core.Network.Protocol.Responses.AbstractResponse import AbstractResponse
from App.Services import PrinterService
from App.Services.Client.MimeFilters import MimeService
from App.Widgets.Components.LoadingAnimation import LoadingAnimation
from App.Widgets.Components.PrintingFileItem import PrintingFileItem
from App.Widgets.Modals.AbstractModal import AbstractModal
from App.Widgets.Modals.ErrorModal import ErrorModal
from App.Widgets.UIHelpers import UIHelpers
from App.helpers import styles, mime, lc, platform, config, network_manager


class PrintingListModal(AbstractModal):
    error_loading_devices_signal = Signal(str)
    checkout_loading_animation_signal = Signal(bool)

    def __init__(self, files: List[QUrl], accepted: List[QUrl], parent: QWidget = None):
        super().__init__(parent)
        self.setWindowFlag(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowTitle(lc("printingListModal.title"))
        self.setMinimumSize(800, 600)
        self.setObjectName("PrintingListModal")
        self.setStyleSheet(styles(["printingListModal", "printingFileItem", "printingLoading"]))

        self.__urls = []
        self.__accepted = accepted
        self.__view_types: dict = config(f'mime.view_types')
        self.__loading_items: int = 0
        self.__devices_loaded = False
        self.__devices: Dict = {}

        self.__error_type_message = lc("printingListModal.unsupported_type_file")

        self.__central_layout = UIHelpers.v_layout((0, 0, 0, 10), 5)

        self.__scroll_area = UIHelpers.create_scroll(self, "PrintingListScrollArea")

        self.__scroll_widget = QWidget(self)
        self.__scroll_widget.setObjectName("PrintingListScrollWidget")

        self.__content_layout = UIHelpers.v_layout((10, 10, 10, 10), 0)

        self.__files_layout = UIHelpers.v_layout((0, 0, 0, 0), 5)

        self.__fill_items(files)

        self.__content_layout.addLayout(self.__files_layout)
        self.__content_layout.addStretch()

        self.__scroll_widget.setLayout(self.__content_layout)

        self.__scroll_area.setWidget(self.__scroll_widget)

        self.__central_layout.addWidget(self.__scroll_area)

        self.__buttons_layout = UIHelpers.h_layout((10, 10, 10, 0), 5)

        # Loading devices block >>>
        self.__loading_devices_widget = QWidget(self)
        self.__loading_devices_widget.setObjectName("PrintingListLoadingDevicesWidget")

        self.__loading_devices_layout = UIHelpers.h_layout((0, 0, 0, 0), 5)
        self.__loading_devices_layout.addWidget(LoadingAnimation((24, 24), (4, 4), self.__loading_devices_widget))

        self.__loading_devices_label = QLabel(self.__loading_devices_widget)
        self.__loading_devices_label.setObjectName("PrintingListLoadingDevicesLabel")
        self.__loading_devices_label.setText(lc("printingListModal.loading_devices_label"))

        self.__loading_devices_layout.addWidget(self.__loading_devices_label)

        self.__loading_devices_widget.setLayout(self.__loading_devices_layout)

        self.__buttons_layout.addWidget(self.__loading_devices_widget)
        # <<< Loading devices block

        # Reload devices button >>>
        self.__reload_devices_button = QPushButton(self)
        self.__reload_devices_button.setObjectName("PrintingListReloadDevicesButton")
        self.__reload_devices_button.setText(lc("printingListModal.reload_devices_button"))
        self.__reload_devices_button.clicked.connect(lambda: self.__start_loading_devices(True))

        self.__buttons_layout.addWidget(self.__reload_devices_button)
        self.__reload_devices_button.hide()
        # <<< Reload devices button

        self.__buttons_layout.addStretch()

        self.__cancel_button = QPushButton(lc("printingListModal.cancel_button"), self)
        self.__cancel_button.setObjectName("PrintingListCancelButton")
        self.__cancel_button.clicked.connect(self.close)
        self.__buttons_layout.addWidget(self.__cancel_button)

        self.__send_button = QPushButton(lc("printingListModal.send_button"), self)
        self.__send_button.setObjectName("PrintingListSendButton")
        self.__send_button.clicked.connect(self.close)
        self.__buttons_layout.addWidget(self.__send_button)

        self.__central_layout.addLayout(self.__buttons_layout)

        self.centralWidget().setLayout(self.__central_layout)

        self.show()

        UIHelpers.to_center_screen(self)

        self.raise_()

        if (self.__loading_items > 0) or not self.__devices_loaded:
            self.__send_button.setDisabled(True)

        self.__start_loading_devices()

    def __fill_devices(self):
        for file_item in self.findChildren(PrintingFileItem):
            file_item: PrintingFileItem
            file_item.set_devices(self.__devices)

    def __open_error_loading_devices(self, message: str):
        if hasattr(self, '__err_modal') and self.__getattribute__('__err_modal'):
            return

        title = lc("errorModal.titles.network")
        message = lc("printingListModal.error_loading_devices") % message
        self.__err_modal = ErrorModal(title, message, self)


    def __set_enable_loading_animation(self, enable: bool):
        self.__loading_devices_widget.setVisible(enable)
        self.__reload_devices_button.setVisible(not enable)

    def __start_loading_devices(self, update_server_cache: bool = False):
        self.__set_enable_loading_animation(True)

        promise = PrinterService.get_printers_promise(ClientConfig.client_ui(), network_manager(), update_server_cache)

        def stop_loading_devices():
            self.checkout_loading_animation_signal.emit(False)

            if not self.__loading_items and self.__devices_loaded:
                self.__send_button.setDisabled(False)

            self.__fill_devices()

            self.error_loading_devices_signal.disconnect()
            self.checkout_loading_animation_signal.disconnect()

        def success_loading_devices(response: AbstractResponse):
            self.__devices_loaded = True

            self.__devices = dict(map(
                lambda x: (x[PrinterService.PRINTER_PARAMETER_NAME], x[PrinterService.PRINTER_PARAMETER_DISPLAY_NAME]),
                PrinterService.filter_hidden_devices(response.data() or [])
            ))

            stop_loading_devices()

        def error_loading_devices(message: str):
            self.error_loading_devices_signal.emit(message)
            stop_loading_devices()

        self.error_loading_devices_signal.connect(self.__open_error_loading_devices)
        self.checkout_loading_animation_signal.connect(self.__set_enable_loading_animation)

        promise.then(success_loading_devices)
        promise.catch(error_loading_devices)

    def __add_loading_item(self):
        self.__loading_items += 1

        if hasattr(self, "__send_button"):
            self.__send_button.setDisabled(True)

    def __pop_loading_item(self):
        self.__loading_items -= 1

        if (not self.__loading_items) and self.__devices_loaded:
            self.__send_button.setDisabled(False)

    def __create_item(self, file: QUrl) -> PrintingFileItem:
        is_windows = platform().is_windows()
        path = file.toLocalFile()

        item = PrintingFileItem({
            PrintingFileItem.PARAMETER_PATH: path.replace(":/", ":\\").replace("/", "\\") if is_windows else path,
            PrintingFileItem.PARAMETER_MIME: self.__view_types.get(mime().get_mime(path)),
            PrintingFileItem.PARAMETER_TYPE_ERROR: False if file in self.__accepted else self.__error_type_message,
        }, self)

        if item.get_need_converting():
            self.__add_loading_item()
            item.converting_stopped.connect(lambda: self.__pop_loading_item())

        return item

    def __fill_items(self, files: List[QUrl]):
        for file in files:
            self.__files_layout.addWidget(self.__create_item(file))

    def __clear_urls(self):
        self.__urls = []
        self.__accepted = []

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            self.__urls = event.mimeData().urls()
            self.__accepted = MimeService.filter_printing_types(self.__urls)

            if self.__accepted:
                event.acceptProposedAction()

        super(PrintingListModal, self).dragEnterEvent(event)

    def dragLeaveEvent(self, event: QDragLeaveEvent):
        self.__clear_urls()

        super(PrintingListModal, self).dragLeaveEvent(event)

    def dropEvent(self, event: QDropEvent):
        for file in self.__urls:
            item = self.__create_item(file)
            item.set_devices(self.__devices)

            self.__files_layout.addWidget(item)

        self.__clear_urls()

        super(PrintingListModal, self).dropEvent(event)
