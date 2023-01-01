"""
Cloe OCR View Components

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
from PyQt5.QtGui import QColor, QMouseEvent
from PyQt5.QtWidgets import QWidget

from components.settings import ViewContainer
from .base import BaseOCRView
from utils.scripts import colorToRGBA


class FullScreenView(BaseOCRView, ViewContainer):
    """
    Fullscreen view with OCR capabilities
    """

    def __init__(self, parent: QWidget):
        super().__init__(parent)

        # Attribute Initializations
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.updateViewStyles(self)

    def setBackgroundColor(self, color: QColor):
        self.setStyleSheet(f"background-color: {colorToRGBA(color)}")

    def mouseReleaseEvent(self, event: QMouseEvent):
        BaseOCRView.mouseReleaseEvent(self, event)
        # Ensure that parent is closed
        self.parent().close()
