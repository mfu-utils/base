from typing import Any, Union, Dict, Optional

from PySide6.QtCore import Qt
from PySide6.QtPdf import QPdfDocument
from PySide6.QtPdfWidgets import QPdfView
from PySide6.QtWidgets import QWidget, QPushButton

from App.Core.Utils import DocumentMediaType, DocumentOrder
from App.Core.Utils.PaperTray import PaperTray
from App.Core.Utils.Ui import Patterns, Casts
from App.Core.Utils.Ui.PrintingPagePolicy import PrintingPagePolicy
from App.Widgets.Components.Controls.LineEditControl import LineEditControl
from App.Widgets.Components.PreferencesControls import PreferencesControls
from App.Widgets.Modals.AbstractModal import AbstractModal
from App.Widgets.UIHelpers import UIHelpers
from App.helpers import lc, platform, styles


class PrintFileParametersModal(AbstractModal):
    PARAMETER_TRANSPARENCY = "transparency"
    PARAMETER_PAGES_POLICY = "pages_policy"
    PARAMETER_PAPER_SIZE = "paper_size"
    PARAMETER_PAPER_TRAY = "paper_tray"
    PARAMETER_LANDSCAPE = "landscape"
    PARAMETER_MIRROR = "mirror"
    PARAMETER_DEVICE = "device"
    PARAMETER_COPIES = "copies"
    PARAMETER_PAGES = "pages"
    PARAMETER_ORDER = "order"

    def __init__(self, path: str, tmp_path: str, parameters: dict, parent: QWidget = None):
        super(PrintFileParametersModal, self).__init__(parent)
        self.setWindowFlag(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
        self.setObjectName("PrintFileParametersModal")
        self.setMinimumSize(600, 500)
        self.setStyleSheet(styles("printFileParametersModal"))

        self.__parameters = parameters.copy()

        self.setWindowTitle(self.__lc("title") % path.split("\\" if platform().is_windows() else "/")[-1])

        self.__central_layout = UIHelpers.h_layout((0, 0, 0, 0), 0)

        self.__document = QPdfDocument()
        self.__document.load(tmp_path)

        self.__doc_view = QPdfView()
        self.__doc_view.setPageMode(QPdfView.PageMode.MultiPage)
        self.__doc_view.setZoomMode(QPdfView.ZoomMode.FitInView)
        self.__doc_view.setDocument(self.__document)

        self.__central_layout.addWidget(self.__doc_view)

        self.__parameters_layout = UIHelpers.v_layout((0, 0, 0, 0), 5)

        self.__scroll_area = UIHelpers.create_scroll(self, "PrintFileParametersScrollArea")

        self.__controls = PreferencesControls(path, self)
        self.__controls.setObjectName("PrintFileParametersControls")
        self.__controls.add_get_value_callback(self.__get_value)
        self.__controls.add_set_value_callback(self.__set_value)
        self.__init_controls()
        self.__controls.generate()

        self.__scroll_area.setWidget(self.__controls)

        self.__parameters_layout.addWidget(self.__scroll_area)

        self.__buttons_layout = UIHelpers.h_layout(spacing=5)
        self.__buttons_layout.addStretch()

        self.__cancel_button = QPushButton(lc("printFileParameters.cancel_button"), self)
        self.__cancel_button.setObjectName("PrintFileParametersCancelButton")
        self.__cancel_button.clicked.connect(self.close)
        self.__buttons_layout.addWidget(self.__cancel_button)

        self.__cancel_button = QPushButton(lc("printFileParameters.save_button"), self)
        self.__cancel_button.setObjectName("PrintFileParametersSaveButton")
        self.__cancel_button.clicked.connect(self.close)
        self.__buttons_layout.addWidget(self.__cancel_button)

        self.__parameters_layout.addLayout(self.__buttons_layout)
        self.__central_layout.addLayout(self.__parameters_layout)

        self.centralWidget().setLayout(self.__central_layout)

        self.show()

        UIHelpers.to_center_screen(self)

        self.raise_()

    def __get_value(self, name: str) -> Any:
        return self.__parameters.get(name)

    def __set_value(self, name: str, value: Any) -> None:
        if isinstance(value, bool):
            value = Casts.bool2str(value)

        self.__parameters[name] = value

    @staticmethod
    def __lc(name: str) -> Union[str, Dict[str, str]]:
        return lc(f"printFileParameters.{name}")

    @staticmethod
    def __clc(control: str, item: str) -> Union[str, Dict[str, str]]:
        return PrintFileParametersModal.__lc(f"controls.{control}.{item}")

    def __init_controls(self):
        label_width = 140
        target_width = 300

        # DEVICE
        device = self.__controls.create_combo_box(self.PARAMETER_DEVICE, self.__clc(self.PARAMETER_DEVICE, "title"), {
            "0": "Xerox WorkCentre 3025",
            "1": "Cannon Direct A4",
        })
        device.label().setFixedWidth(label_width)
        device.target().setFixedWidth(target_width)

        # COPIES
        copies = self.__controls.create_spinbox(
            self.PARAMETER_COPIES, self.__clc(self.PARAMETER_COPIES, "title"), (1, 999)
        )
        copies.label().setFixedWidth(label_width)
        copies.target().setFixedWidth(target_width)

        # PAPER SIZE
        media = self.__controls.create_combo_box(
            self.PARAMETER_PAPER_SIZE,
            self.__clc(self.PARAMETER_PAPER_SIZE, "title"),
            Casts.enum2dict(DocumentMediaType)
        )
        media.label().setFixedWidth(label_width)
        media.target().setFixedWidth(target_width)

        # PAPER TRAY
        # noinspection PyTypeChecker
        paper_tray = self.__controls.create_combo_box(
            self.PARAMETER_PAPER_TRAY,
            self.__clc(self.PARAMETER_PAPER_TRAY, "title"),
            {
                None: self.__clc(self.PARAMETER_PAPER_TRAY, "default"),
                **Casts.enum2dict(PaperTray, self.__lc("paper_tray_items"))
            }
        )
        paper_tray.label().setFixedWidth(label_width)
        paper_tray.target().setFixedWidth(target_width)

        # ORDER
        order = self.__controls.create_combo_box(
            self.PARAMETER_ORDER,
            self.__clc(self.PARAMETER_ORDER, "title"),
            Casts.enum2dict(DocumentOrder),
        )
        order.label().setFixedWidth(label_width)
        order.target().setFixedWidth(target_width)

        pages: Optional[LineEditControl] = None

        # PRINTING PAGES
        pages_policy = self.__controls.create_combo_box(
            self.PARAMETER_PAGES_POLICY,
            self.__clc(self.PARAMETER_PAGES_POLICY, "title"),
            printing_pages_policies := Casts.enum2dict(PrintingPagePolicy)
        )
        pages_policy.label().setFixedWidth(label_width)
        pages_policy.target().setFixedWidth(target_width)

        printing_pages_policies_keys = list(printing_pages_policies.keys())

        # noinspection PyUnresolvedReferences
        pages_policy.target().currentIndexChanged.connect(
            lambda x: pages.setVisible(printing_pages_policies_keys[x] == PrintingPagePolicy.Custom.value)
        )

        # PAGES
        pages = self.__controls.create_line_edit(self.PARAMETER_PAGES, "")
        pages.set_description(self.__clc(self.PARAMETER_PAGES, "description"))
        pages.pattern_set(
            "cups_format", Patterns.PRINTING_PAGE_PATTERN, self.__clc(self.PARAMETER_PAGES, "cups_format_error")
        )
        pages.pattern_enable("cups_format")
        pages.label().setFixedWidth(label_width)
        pages.setVisible(self.__parameters[self.PARAMETER_PAGES_POLICY] == PrintingPagePolicy.Custom.value)

        # MIRROR
        self.__controls.create_check_box(self.PARAMETER_MIRROR, self.__clc(self.PARAMETER_MIRROR, "title"))

        # LANDSCAPE
        self.__controls.create_check_box(self.PARAMETER_LANDSCAPE, self.__clc(self.PARAMETER_LANDSCAPE, "title"))

        # TRANSPARENCY
        self.__controls.create_check_box(self.PARAMETER_TRANSPARENCY, self.__clc(self.PARAMETER_TRANSPARENCY, "title"))
