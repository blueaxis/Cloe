"""
Cloe Window Components

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

from typing import TYPE_CHECKING

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCloseEvent, QCursor
from PyQt5.QtWidgets import QApplication, QMainWindow

from components.views import FullScreenView

if TYPE_CHECKING:
    from .tray import SystemTray


class ExternalWindow(QMainWindow):
    """
    External window widget to enclose FullScreenView
    """

    def __init__(self, parent: "SystemTray"):
        super().__init__()

        # Layout and styles
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet("border:0px; margin:0px")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Popup)
        self.setAttribute(Qt.WA_NoSystemBackground)
        self.setAttribute(Qt.WA_TranslucentBackground)
        QApplication.setOverrideCursor(QCursor(Qt.CrossCursor))

        self.setCentralWidget(FullScreenView(self))
        self.ocrModel = parent.ocrModel

    def closeEvent(self, event: QCloseEvent):
        # Ensure that object is deleted before closing
        self.deleteLater()
        # Restore cursor
        QApplication.restoreOverrideCursor()
        return super().closeEvent(event)
