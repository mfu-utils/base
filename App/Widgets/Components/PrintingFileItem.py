from typing import Optional

from PySide6.QtWidgets import QWidget, QLabel, QPushButton

from App.Core.Utils import DocumentMediaType, DocumentOrder
from App.Core.Utils.Ui.PrintingPagePolicy import PrintingPagePolicy
from App.Services.MimeConvertor import MimeConvertor
from App.Widgets.Components.DrawableWidget import DrawableWidget
from App.Widgets.Components.LoadingAnimation import LoadingAnimation
from App.Widgets.Modals.PrintFileParametersModal import PrintFileParametersModal
from App.Widgets.UIHelpers import UIHelpers
from App.helpers import icon, mime_convertor, ini, styles, in_thread


class PrintingFileItem(DrawableWidget):
    PARAMETER_TYPE_ERROR = "type_error"
    PARAMETER_INDEX = "index"
    PARAMETER_PATH = "path"
    PARAMETER_MIME = "mime"

    PRINTING_PARAMETERS = {
        PrintFileParametersModal.PARAMETER_DEVICE: "0",
        PrintFileParametersModal.PARAMETER_PAGES: "",
        PrintFileParametersModal.PARAMETER_COPIES: 1,
        PrintFileParametersModal.PARAMETER_PAPER_TRAY: None,
        PrintFileParametersModal.PARAMETER_PAGES_POLICY: PrintingPagePolicy.All.value,
        PrintFileParametersModal.PARAMETER_PAPER_SIZE: DocumentMediaType.A4.value,
        PrintFileParametersModal.PARAMETER_ORDER: DocumentOrder.Normal.value,
        PrintFileParametersModal.PARAMETER_MIRROR: "False",
        PrintFileParametersModal.PARAMETER_LANDSCAPE: "False",
    }

    def __init__(self, parameters: dict, parent: QWidget = None):
        super(PrintingFileItem, self).__init__(parent)
        self.setObjectName('PrintingFileItem')

        self.__parameters = parameters
        self.__converted_path: Optional[str] = self.__parameters[self.PARAMETER_PATH][:]

        type_error = parameters.get(self.PARAMETER_TYPE_ERROR) or False

        self.__need_converting = False

        if ini('printing.view_tool') in MimeConvertor.suits_values(False):
            self.__need_converting = True

        self.__central_layout = UIHelpers.h_layout((10, 3, 10, 3), 5)

        self.__index_widget = QLabel(f"{str(parameters[self.PARAMETER_INDEX])}.", self)
        self.__index_widget.setObjectName("PrintingFileItemIndex")
        self.__central_layout.addWidget(self.__index_widget)
        self.__central_layout.addSpacing(10)

        self.__content_layout = UIHelpers.v_layout((0, 0, 0, 0), 5)

        self.__title = QLabel(parameters[self.PARAMETER_PATH], self)
        self.__title.setObjectName('PrintingFileItemTitle')

        if type_error:
            self.__title.setDisabled(True)

        self.__content_layout.addWidget(self.__title)

        self.__parameters_layout = UIHelpers.h_layout((0, 0, 0, 0), 2)

        if type_error:
            self.__error_type_icon = UIHelpers.image("error_sign_16x16@2x.png")
            self.__error_type_icon.setObjectName("PrintingFileItemErrorTypeIcon")
            self.__error_type_icon.setDisabled(True)
            self.__parameters_layout.addWidget(self.__error_type_icon)

            self.__parameters_layout.addSpacing(5)

            self.__error_type_message = QLabel(parameters[self.PARAMETER_TYPE_ERROR], self)
            self.__error_type_message.setObjectName("PrintingFileItemErrorTypeMessage")
            self.__error_type_message.setDisabled(True)
            self.__parameters_layout.addWidget(self.__error_type_message)
            self.__loading_block = None
        else:
            self.__loading_block = self.__create_loading_block()
            self.__parameters_layout.addWidget(self.__loading_block)

        self.__mime_widget = QLabel(parameters[self.PARAMETER_MIME], self)
        self.__mime_widget.setObjectName('PrintingFileItemMime')

        if type_error:
            self.__mime_widget.setDisabled(True)
            self.__content_layout.addWidget(self.__mime_widget)
        else:
            self.__parameters_layout.addWidget(self.__mime_widget)

        self.__parameters_layout.addStretch()

        self.__content_layout.addLayout(self.__parameters_layout)

        self.__central_layout.addLayout(self.__content_layout)

        self.__central_layout.addStretch()

        self.__parameters_button = self.__create_button(
            "PrintingFileItemParametersButton", "gear.png", self.__open_parameters_modal
        )
        self.__central_layout.addWidget(self.__parameters_button)

        self.__delete_button = self.__create_button("PrintingFileItemDeleteButton", "bin.png", self.deleteLater)
        self.__central_layout.addWidget(self.__delete_button)

        self.setLayout(self.__central_layout)

        self.setProperty("warning", bool(type_error))

        if not type_error:
            self.setDisabled(True)

            if self.__need_converting:
                self.__start_converting()

            UIHelpers.update_style(self)

    def __create_loading_block(self) -> QWidget:
        widget = DrawableWidget(self)

        layout = UIHelpers.h_layout((0, 0, 10, 0), 5)

        animation = LoadingAnimation((16, 16), (4, 4), widget)
        animation.setStyleSheet(styles("loadingAnimation"))
        layout.addWidget(animation)

        layout.setSpacing(5)

        label = QLabel(self)
        label.setObjectName("PrintingFileItemLoadingText")
        label.setText("Loading...")
        layout.addWidget(label)

        widget.setLayout(layout)

        return widget

    def __open_parameters_modal(self):
        PrintFileParametersModal(
            self.__parameters[self.PARAMETER_PATH],
            self.__converted_path,
            self.PRINTING_PARAMETERS,
            self
        )

    def path(self) -> str:
        return self.__parameters[self.PARAMETER_PATH]

    def error(self) -> bool:
        return bool(self.__parameters[self.PARAMETER_TYPE_ERROR])

    def __create_button(self, name: str, _icon: str, callback: callable = None) -> QPushButton:
        button = QPushButton(self)
        button.setFixedSize(30, 30)
        button.setObjectName(name)
        button.setIcon(icon(_icon))

        if callback:
            button.clicked.connect(callback)

        return button

    def __start_converting(self):
        def _worker():
            suit = MimeConvertor.OfficeSuit(ini('printing.view_tool'))

            self.__converted_path = mime_convertor().get_pdf(self.__parameters[self.PARAMETER_PATH], suit)
            self.setEnabled(True)

            self.__loading_block.deleteLater()

            UIHelpers.update_style(self)

        in_thread(_worker)
