from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QApplication

from App.Core.Ui.TrayButton import TrayButton
from App.Widgets.Components.Tools.ScanTools import ScanTools
from App.helpers import lc, platform, config


class Tray(TrayButton):
    def __init__(self, app: QApplication, parent: QWidget = None):
        self.__light = (app.styleHints().colorScheme() != Qt.ColorScheme.Dark) or platform().is_darwin()

        super(Tray, self).__init__("printer_dark" if self.__light else "printer", parent)

        self.add_action(config('app.name'), callback=parent.show)
        self.add_separator()
        self.add_action(lc('tray.scan'), callback=lambda: ScanTools(parent).create_scan())
        self.add_separator()
        self.add_action(lc('tray.quit'), callback=app.quit)
