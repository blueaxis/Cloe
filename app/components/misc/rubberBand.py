"""
Cloe Rubberband Component

Copyright (C) `2021-2022` `<Alarcon Ace Belen>`

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPainter, QPaintEvent, QPen
from PyQt5.QtWidgets import QRubberBand, QWidget


class RubberBand(QRubberBand):
    """Rubberband object that can be customized

    Args:
        parent (QWidget): Widget where the rubberband is shown
        shape (Shape, optional): Rubberband shape. Defaults to Rectangle.
        thickness (int, optional): Rubberband border thickness. Defaults to 2.
        borderColor (QColor, optional): Rubberband border color. Defaults to blue.
        fillColor (QColor, optional): Rubberband fill color. Defaults to QColor(0, 128, 255, 60).
    """

    def __init__(
        self,
        parent: QWidget,
        shape: QRubberBand.Shape = QRubberBand.Rectangle,
        thickness=2,
        borderColor: QColor = Qt.blue,
        fillColor=QColor(0, 128, 255, 60),
    ):
        super().__init__(shape, parent)
        self.setBorder(borderColor, thickness)
        self.setFill(fillColor)

    def setBorder(self, color: QColor, thickness: int):
        self._borderColor = color
        self._borderThickness = thickness

    def setFill(self, color: QColor):
        self._fillColor = color

    def paintEvent(self, event: QPaintEvent):
        painter = QPainter()
        painter.begin(self)
        # Mask
        painter.fillRect(event.rect(), self._fillColor)
        # Border
        painter.setPen(QPen(self._borderColor, self._borderThickness))
        painter.drawRect(event.rect())
        painter.end()
        # return super().paintEvent(event)
