from typing import List

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QUrl

from App.Widgets.Modals.PrintParametersModal import PrintParametersModal
from App.Widgets.UIHelpers import UIHelpers


class PrintingTools:
    @staticmethod
    def open_printing_parameters_modal(files: List[QUrl], accepted: List[QUrl], parent: QWidget = None):
        PrintParametersModal(files, accepted, UIHelpers.get_main_window(parent))
