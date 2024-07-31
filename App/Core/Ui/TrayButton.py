from PySide6.QtGui import QAction
from PySide6.QtWidgets import QWidget, QSystemTrayIcon, QMenu
from App.helpers import icon


class TrayButton:
    def __init__(self, _icon: str, parent: QWidget = None):
        self._parent = parent

        self._tray = QSystemTrayIcon(icon(_icon), parent)
        self._tray.setVisible(True)

        self._menu = QMenu()

    def add_action(self, title: str, _icon: str = None, callback: callable = None):
        action = QAction(title, self._menu)

        if _icon:
            action.setIcon(icon(_icon))

        if callback:
            action.triggered.connect(callback)

        self._menu.addAction(action)

        return action

    def add_separator(self):
        self._menu.addSeparator()

    def show(self):
        self._tray.setContextMenu(self._menu)
