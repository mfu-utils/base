import math
from typing import Optional

from PySide6.QtCore import Qt, QVariantAnimation, QSize, QEasingCurve
from PySide6.QtWidgets import QWidget, QLabel

from App.Widgets.UiHelpers import UiHelpers

from App.helpers import styles
from App.Widgets.Modals.AbstractModal import AbstractModal


class LoadingModal(AbstractModal):
    def __init__(self, text: Optional[str] = None, parent: QWidget = None):
        super(LoadingModal, self).__init__(parent)
        self._frameless_window(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self._d8d(False)

        if not parent:
            self.setWindowFlags(self.windowFlags() | Qt.WindowType.Tool)

        self.setObjectName('LoadingModal')
        self.setStyleSheet(styles('loadingModal'))

        self.__movable_size = QSize(6, 6)
        self.__container_size = QSize(60, 60)
        self.__start_position = (0.0, self.__container_size.height() / 2 - self.__movable_size.height())
        self.__center_pos = (self.__container_size.width() / 2, self.__container_size.height() / 2)

        self.centralWidget().setObjectName('Loading')

        self.__central_layout = UiHelpers.h_layout()
        self.__central_layout.addStretch()

        self.__content_layout = UiHelpers.v_layout()

        self.__container_layout = UiHelpers.h_layout((0, 0, 0, 0), 0)
        self.__container_layout.addStretch()
        self.__container_layout.addWidget(self.__create_animated_widget())
        self.__container_layout.addStretch()

        self.__content_layout.addLayout(self.__container_layout)

        if text:
            label = QLabel(text, self)
            label.setObjectName('LoadingText')

            self.__content_layout.addWidget(label)

            self.__central_layout.addLayout(self.__content_layout)

        self.__central_layout.addStretch()

        self.centralWidget().setLayout(self.__central_layout)

        self.show()

        if not parent:
            UiHelpers.to_center_screen(self)
        else:
            UiHelpers.to_center(self)

    def __create_animated_widget(self) -> QWidget:
        container = QWidget(self)
        container.setObjectName('Container')
        container.setFixedSize(self.__container_size)

        transformed_widget = QWidget(container)
        transformed_widget.setObjectName('TransformedWidget')
        transformed_widget.setFixedSize(self.__movable_size)

        transformed_widget.move(int(self.__center_pos[0]), self.__movable_size.height())

        self.__create_animation(transformed_widget)

        return container

    def __create_animation(self, widget: QWidget):
        animation = QVariantAnimation(widget)
        animation.setDuration(1000)
        animation.setStartValue(360)
        animation.setEndValue(0)
        animation.valueChanged.connect(lambda x: self.__rotate_angle(widget, x))
        animation.setEasingCurve(QEasingCurve.Type.InOutSine)
        animation.setLoopCount(-1)
        animation.start()

    def __rotate_angle(self, widget: QWidget, angle: int):
        pos = self.__start_position

        x = pos[0] * math.cos(math.radians(angle)) - pos[1] * math.sin(math.radians(angle))
        y = pos[0] * math.sin(math.radians(angle)) + pos[1] * math.cos(math.radians(angle))

        widget.move(int(self.__center_pos[0] + x), int(self.__center_pos[1] - y))
