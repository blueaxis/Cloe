"""
Cloe Preview Component

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

from PyQt5.QtCore import (Qt)
from PyQt5.QtGui import (QColor, QPainter, QPaintEvent, QPen, QResizeEvent)
from PyQt5.QtWidgets import (QLabel, QGridLayout, QWidget)

from components.misc import RubberBand


class Preview(QWidget):
    """
    Widget to allow preview of view settings changes
    """

    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setObjectName("liveView")
        self.setLayout(QGridLayout(self))

        self.createPreviewText()
        self.createSelectionBand()

    def setBackgroundColor(self, color: QColor):
        self.backgroundColor = color

# -------------------------------- UI Initializations -------------------------------- #

    def createSelectionBand(self):
        self.rubberBand = RubberBand(self)
        self.rubberBand.show()

    def createPreviewText(self, text="Sample Text"):
        self._previewText = QLabel(text)
        self._previewText.setObjectName("previewText")
        self._previewText.adjustSize()
        self.layout().addWidget(self._previewText, 0, 0,
                                alignment=Qt.AlignTop | Qt.AlignLeft)

    def createAlphaBackground(self):
        painter = QPainter()
        painter.begin(self)

        # Draw alpha background
        # Adopted from: https://sourceforge.net/projects/capture2text/
        squareSize = 20
        numSquaresX = int(self.width() / squareSize) + 1
        numSquaresY = int(self.height() / squareSize) + 1
        for y in range(numSquaresY):
            isWhite = ((y % 2) == 0)
            for x in range(numSquaresX):
                color = QColor(200, 200, 200, 255)
                if(isWhite):
                    color.setRgb(255, 255, 255, 255)
                painter.fillRect(x * squareSize, y * squareSize,
                                 squareSize, squareSize, color)
                isWhite = not isWhite
        # Draw true background
        painter.fillRect(0, 0, self.width(), self.height(), self.backgroundColor)
        # Draw border
        painter.setPen(QPen(QColor(0, 0, 0), 2))
        painter.drawRect(0, 0, self.width(), self.height())

    def paintEvent(self, event: QPaintEvent):
        self.createAlphaBackground()
        return super().paintEvent(event)

# ----------------------------------- View Updates ----------------------------------- #

    def resizeEvent(self, event: QResizeEvent):
        if self is not None:
            # Resize rubber band when window size is changed
            w = 0.4 * self.width()
            y = 0.05 * self.height()
            x = self.width() - w - y
            h = self.height() - 2*y
            self.rubberBand.setGeometry(x, y, w, h)
        return super().resizeEvent(event)
