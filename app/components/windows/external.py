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
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QMainWindow

from components.views import FullScreenView

if TYPE_CHECKING:
    from .tray import SystemTray


class ExternalWindow(QMainWindow):
    """
    External window widget to enclose FullScreenView
    """

    def __init__(self, parent: "SystemTray"):
        super().__init__()
        self.systemTray = parent

        # By setting the border thickness and margin to zero,
        # we ensure that the whole screen is captured.
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet("border:0px; margin:0px")

        # Enables the widget to have a transparent background.
        self.setAttribute(Qt.WA_NoSystemBackground)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # FramelessWindowHint flag also enables transparent background.
        # WindowStaysOnTopHint & Popup flags ensures that the widget is the top window.
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Popup)

        self.setCentralWidget(FullScreenView(self))
        self.ocrModel = parent.ocrModel

    def showFullScreen(self):
        # Overridden to show on the active screen
        fullscreen: FullScreenView = self.centralWidget()
        screenIndex = fullscreen.getActiveScreenIndex()

        # TODO: Find an alternative way to show the active screen,
        # since QDesktopWidget is obsolete according to Qt docs
        screen = QDesktopWidget().screenGeometry(screenIndex)
        self.move(screen.left(), screen.top())

        QApplication.setOverrideCursor(QCursor(Qt.CrossCursor))

        return super().showFullScreen()

    def closeEvent(self, event: QCloseEvent):
        # Ensure that object is deleted before closing
        self.deleteLater()
        self.systemTray.externalWindow = None
        # Restore cursor
        QApplication.restoreOverrideCursor()
        return super().closeEvent(event)
