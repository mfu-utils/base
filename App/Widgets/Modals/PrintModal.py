from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QDropEvent, QDragLeaveEvent, QDragEnterEvent
from PySide6.QtWidgets import QWidget, QLabel, QPushButton

from App.Widgets.Modals.AbstractModal import AbstractModal
from App.Widgets.UIHelpers import UIHelpers
from App.helpers import styles, lc


class PrintModal(AbstractModal):
    closed = Signal()

    def __init__(self, parent: QWidget = None):
        super(PrintModal, self).__init__(parent)
        self._frameless_window(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self._d8d(False)
        self.set_shadow_enabled(False)
        self.setFixedSize(200, 200)
        self.centralWidget().setObjectName("PrintModal")
        self.setStyleSheet(styles("printModal"))

        self.__central_Layout = UIHelpers.v_layout(spacing=0)

        self.__headers = UIHelpers.h_layout((0, 0, 0, 0), 3)

        self.__close_button = QPushButton("X")
        self.__close_button.setFixedSize(16, 16)
        self.__close_button.setObjectName("PrintModalCloseButton")
        self.__close_button.clicked.connect(self.close)

        self.__headers.addStretch()
        self.__headers.addWidget(self.__close_button)

        self.__central_Layout.addLayout(self.__headers)

        self.__central_Layout.addStretch()

        self.__message = QLabel(lc("printingModal.message"), self)
        self.__message.setObjectName("PrintModalMessage")
        self.__message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.__central_Layout.addWidget(self.__message)

        self.__central_Layout.addStretch()

        self.centralWidget().setLayout(self.__central_Layout)

        self.show()

    def closeEvent(self, event):
        self.closed.emit()

        super(PrintModal, self).closeEvent(event)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            print(urls)
            print(event.mimeData().formats())
        # TODO: Create transparent layer with info
        super(PrintModal, self).dragEnterEvent(event)

    def dragLeaveEvent(self, event: QDragLeaveEvent):
        # TODO: Hide transparent layer
        super(PrintModal, self).dragLeaveEvent(event)

    def dropEvent(self, event: QDropEvent):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            print(urls)
            pass
        # TODO: Determinate image and get path for open document modal
        super(PrintModal, self).dropEvent(event)
