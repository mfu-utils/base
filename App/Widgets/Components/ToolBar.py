from PySide6.QtCore import QSize
from PySide6.QtWidgets import QWidget, QPushButton

from App.Widgets.Components.DrawableWidget import DrawableWidget
from App.Widgets.Components.Notifications.NotificationButton import NotificationButton
from App.Widgets.Components.Tools.ScanTools import ScanTools
from App.Widgets.Modals.PreferencesModal import PreferencesModal
from App.Widgets.Modals.ScanListModal import ScanListModal
from App.Widgets.Modals.TagsListModal import TagsListModal
from App.Widgets.UIHelpers import UIHelpers

from App.helpers import icon, styles, lc, events
from App.Widgets.Modals.ScanTypesListModal import ScanTypesListModal


class ToolBar(DrawableWidget):
    def __init__(self, parent: QWidget = None):
        super(ToolBar, self).__init__(parent)
        self.setObjectName('ToolBar')
        self.setStyleSheet(styles('toolBar'))

        self.__central_layout = UIHelpers.v_layout((5, 5, 5, 5), 5)

        # Top
        self.__create_tool_button('create.png', 'ToolBarScanNewButton', lc('toolBar.new_scan'), self.create_scan)
        self.__create_tool_button('add_image.png', 'ToolBarAddImageButton', lc('toolBar.add_image'), self.add_image)
        self.__create_tool_button('stack.png', 'ToolBarOpenScanTypes', lc('toolBar.scan_types'), self.open_scan_types)
        self.__create_tool_button('tag.png', 'ToolBarOpenTags', lc('toolBar.tags'), self.open_tags)
        self.__create_tool_button('scanned.png', 'ToolBarOpenScanList', lc('toolBar.scan_list'), self.open_scan_list)
        # self.__create_tool_button('docs.png', 'ToolBarDocsButton', lc('toolBar.docs'), lambda: print(1))

        self.__central_layout.addStretch()

        # Bottom
        self.__create_tool_button(
            'bell.png',
            'ToolBarNotifications',
            lc('toolBar.notifications'),
            lambda: events().fire("notification-widget-checkout"),
            NotificationButton
        )
        self.__create_tool_button(
            'settings.png',
            'ToolBarScanSettingsButton',
            lc('toolBar.preferences'),
            self.open_preferences_modal
        )

        self.setLayout(self.__central_layout)

    def create_scan(self):
        ScanTools(self).create_scan()

    def add_image(self):
        ScanTools(self).image_scan()

    def open_scan_types(self):
        ScanTypesListModal(self)

    def open_tags(self):
        TagsListModal(self)

    def open_preferences_modal(self):
        PreferencesModal(self)

    def open_scan_list(self):
        ScanListModal(self)

    def __create_tool_button(self, _icon: str, name: str, title: str, handle: callable, _type=QPushButton) -> QPushButton:
        button = _type(self)
        button.setIcon(icon(_icon))
        button.setIconSize(QSize(32, 32))
        button.setObjectName(name)
        button.setFixedSize(32, 32)
        button.clicked.connect(handle)
        button.setToolTip(title)

        self.__central_layout.addWidget(button)

        return button
