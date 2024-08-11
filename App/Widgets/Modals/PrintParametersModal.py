from typing import List

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QUrl

from App.Widgets.Components.PrintingFileItem import PrintingFileItem
from App.Widgets.Modals.AbstractModal import AbstractModal
from App.Widgets.UIHelpers import UIHelpers
from App.helpers import styles, mime, lc


class PrintParametersModal(AbstractModal):
    def __init__(self, files: List[QUrl], parent: QWidget = None):
        super().__init__(parent)
        self.setWindowTitle(lc("printingParametersModal.title"))
        self.setMinimumSize(600, 400)
        self.setObjectName("PrintParametersModal")
        self.setStyleSheet(styles(["printParametersModal", "printingFileItem"]))

        self.__central_layout = UIHelpers.v_layout((5, 5, 5, 5), 5)

        self.__files_layout = UIHelpers.v_layout((0, 0, 0, 0), 0)

        self.__fill_items(files)

        self.__central_layout.addLayout(self.__files_layout)

        self.__central_layout.addStretch()

        self.centralWidget().setLayout(self.__central_layout)

        self.show()

        UIHelpers.to_center_screen(self)

        self.raise_()

    def __fill_items(self, files: List[QUrl]):
        for i, file in enumerate(files, start=1):
            path = file.toLocalFile()

            self.__files_layout.addWidget(PrintingFileItem({
                PrintingFileItem.PARAMETER_PATH: path,
                PrintingFileItem.PARAMETER_MIME: mime().get_mime(path),
                PrintingFileItem.PARAMETER_INDEX: i,
            }, self))
