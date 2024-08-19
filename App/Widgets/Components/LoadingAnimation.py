from typing import Tuple

import math
from PySide6.QtCore import QVariantAnimation, QEasingCurve
from PySide6.QtWidgets import QWidget

from App.Widgets.Components.DrawableWidget import DrawableWidget


class LoadingAnimation(DrawableWidget):
    def __init__(self, size: Tuple[int, int], movable_size: Tuple[int, int], parent: QWidget = None):
        super(LoadingAnimation, self).__init__(parent)

        self.setObjectName('LoadingContainer')
        self.setFixedSize(size[0], size[1])

        transformed_widget = QWidget(self)
        transformed_widget.setObjectName('LoadingTransformedWidget')
        transformed_widget.setFixedSize(movable_size[0], movable_size[1])

        self.__start_pos = (0, self.height() / 2 - movable_size[1])

        transformed_widget.move(int(self.__start_pos[0]), int(self.__start_pos[1]))

        self.__create_animation(transformed_widget)

        self.__center_pos = (self.width() / 2, self.height() / 2)

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
        pos = self.__start_pos

        x = pos[0] * math.cos(math.radians(angle)) - pos[1] * math.sin(math.radians(angle))
        y = pos[0] * math.sin(math.radians(angle)) + pos[1] * math.cos(math.radians(angle))

        widget.move(int(self.__center_pos[0] + x), int(self.__center_pos[1] - y))
