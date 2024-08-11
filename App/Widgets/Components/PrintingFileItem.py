from PySide6.QtWidgets import QWidget, QLabel

from App.Widgets.Components.DrawableWidget import DrawableWidget
from App.Widgets.UIHelpers import UIHelpers


class PrintingFileItem(DrawableWidget):
    PARAMETER_PATH = "path"
    PARAMETER_MIME = "mime"
    PARAMETER_INDEX = "index"

    def __init__(self, parameters: dict,  parent: QWidget = None):
        super(PrintingFileItem, self).__init__(parent)
        self.setObjectName('PrintingFileItem')

        self.__central_layout = UIHelpers.h_layout((10, 3, 10, 3), 15)

        self.__index_widget = QLabel(f"{str(parameters[self.PARAMETER_INDEX])}.", self)
        self.__index_widget.setObjectName("PrintingFileItemIndex")
        self.__central_layout.addWidget(self.__index_widget)

        self.__content_layout = UIHelpers.v_layout((0, 0, 0, 0), 5)

        self.__title = QLabel(parameters[self.PARAMETER_PATH], self)
        self.__title.setObjectName('PrintingFileItemTitle')
        self.__content_layout.addWidget(self.__title)

        self.__parameters_layout = UIHelpers.h_layout((0, 0, 0, 0), 2)

        self.__mime_widget = QLabel(parameters[self.PARAMETER_MIME], self)
        self.__mime_widget.setObjectName('PrintingFileItemMime')
        self.__parameters_layout.addWidget(self.__mime_widget)

        self.__parameters_layout.addStretch()

        self.__content_layout.addLayout(self.__parameters_layout)

        self.__central_layout.addLayout(self.__content_layout)

        self.__central_layout.addStretch()

        self.setLayout(self.__central_layout)
