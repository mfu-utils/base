from typing import List

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QUrl, Qt

from App.Widgets.Components.PrintingFileItem import PrintingFileItem
from App.Widgets.Modals.AbstractModal import AbstractModal
from App.Widgets.UIHelpers import UIHelpers
from App.helpers import styles, mime, lc, platform


class PrintParametersModal(AbstractModal):
    def __init__(self, files: List[QUrl], accepted: List[QUrl], parent: QWidget = None):
        super().__init__(parent)
        self.setWindowFlag(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowTitle(lc("printingParametersModal.title"))
        self.setMinimumSize(600, 400)
        self.setObjectName("PrintParametersModal")
        self.setStyleSheet(styles(["printParametersModal", "printingFileItem"]))

        self.__accepted = accepted

        self.__error_type_message = lc("printingParametersModal.error_type_file")

        self.__central_layout = UIHelpers.h_layout((5, 5, 5, 5), 5)

        self.__scroll_area = UIHelpers.create_scroll(self, "PrintParametersScrollArea")

        self.__scroll_widget = QWidget(self)
        self.__scroll_widget.setObjectName("PrintParametersScrollWidget")

        self.__content_layout = UIHelpers.v_layout((0, 0, 0, 0), 0)

        self.__files_layout = UIHelpers.v_layout((0, 0, 0, 0), 5)

        self.__fill_items(files)

        self.__content_layout.addLayout(self.__files_layout)
        self.__content_layout.addStretch()

        self.__scroll_widget.setLayout(self.__content_layout)

        self.__scroll_area.setWidget(self.__scroll_widget)

        self.__central_layout.addWidget(self.__scroll_area)

        self.centralWidget().setLayout(self.__central_layout)

        self.show()

        UIHelpers.to_center_screen(self)

        self.raise_()

    def __fill_items(self, files: List[QUrl]):
        is_windows = platform().is_windows()

        for i, file in enumerate(files, start=1):
            path = file.toLocalFile()

            self.__files_layout.addWidget(PrintingFileItem({
                PrintingFileItem.PARAMETER_PATH: path.replace(":/", ":\\").replace("/", "\\") if is_windows else path,
                PrintingFileItem.PARAMETER_MIME: mime().get_mime(path),
                PrintingFileItem.PARAMETER_INDEX: i,
                PrintingFileItem.PARAMETER_TYPE_ERROR: False if file in self.__accepted else self.__error_type_message,
            }, self))
