"""
Cloe Main Application

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

from manga_ocr import MangaOcr
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import (QThreadPool)
from PyQt5.QtWidgets import (QSystemTrayIcon, QMenu, QApplication)

from Workers import BaseWorker
from Views import ExternalWindow
from Settings import SettingsMenu
from Popups import AboutPage


class SystemTrayApp(QSystemTrayIcon):

    def __init__(self, parent=None):
        icon = QIcon("./assets/images/icons/logo.ico")
        QSystemTrayIcon.__init__(self, icon, parent)

        # State trackers and configurations
        self.threadpool = QThreadPool()
        self.ocrModel = None

        # Menu
        menu = QMenu(parent)
        self.setContextMenu(menu)

        # Menu Actions
        menu.addAction(QIcon("./assets/images/icons/settings.png"),
            "Settings", self.openSettings)
        menu.addSeparator()
        menu.addAction(QIcon("./assets/images/icons/about.png"),
            "About Chloe", self.openAbout)
        menu.addAction(QIcon("./assets/images/icons/exit.png"),
            "Exit", self.closeApplication)

    def loadModel(self):
        def loadModelHelper():
            import http.client as httplib

            def isConnected(url="8.8.8.8"):
                connection = httplib.HTTPSConnection(url, timeout=2)
                try:
                    connection.request("HEAD", "/")
                    return True
                except Exception:
                    return False
                finally:
                    connection.close()

            connected = isConnected()
            if connected:
                self.showMessage("Please wait",
                                 "Loading the MangaOCR model ...")
                self.ocrModel = MangaOcr()
            return connected

        def modelLoadedConfirmation(connected):
            if connected:
                self.showMessage("MangaOCR model loaded",
                    "You are now using the MangaOCR model for Japanese text detection.")
            elif not connected:
                self.showMessage("Connection Error",
                    "Please try again or make sure your Internet connection is on.")

        worker = BaseWorker(loadModelHelper)
        worker.signals.result.connect(modelLoadedConfirmation)
        self.threadpool.start(worker)

    def startCapture(self):

        if self.ocrModel == None:
            self.showMessage(
                "MangaOCR model not yet loaded",
                "Please wait until the MangaOCR model is loaded."
            )
            return
        self.externalWindow = ExternalWindow(self)
        self.externalWindow.showFullScreen()

    def openSettings(self):
        self.settingsMenu = SettingsMenu()
        self.settingsMenu.show()
    
    def openAbout(self):
        AboutPage().exec()

    def closeApplication(self):
        QApplication.instance().exit()
