"""
Poricom Main Window Component

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

from shutil import rmtree
from time import sleep

import toml
from manga_ocr import MangaOcr
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import (Qt, QAbstractNativeEventFilter, QThreadPool)
from PyQt5.QtWidgets import (QSystemTrayIcon, QMenu, QWidgetAction,
    QVBoxLayout, QWidget, QMainWindow, QApplication)


from utils.config import config, saveOnClose
from Workers import BaseWorker
from Ribbon import (Ribbon)
from Views import (ExternalWindow)
from Popups import (ShortcutPicker, FontPicker, PickerPopup, MessagePopup)


class WinEventFilter(QAbstractNativeEventFilter):
    def __init__(self, keybinder):
        self.keybinder = keybinder
        super().__init__()

    def nativeEventFilter(self, eventType, message):
        ret = self.keybinder.handler(eventType, message)
        return ret, 0


class SystemTrayApp(QSystemTrayIcon):

    def __init__(self, parent=None, tracker=None):
        icon = QIcon("./assets/images/icons/logo.ico")
        QSystemTrayIcon.__init__(self, icon, parent)

        # State trackers and configurations
        self.tracker = tracker
        self.config = config
        self.threadpool = QThreadPool()

        # Menu
        menu = QMenu(parent)
        self.setContextMenu(menu)

        # Menu Actions
        settingsAction = menu.addAction("Settings")
        settingsAction.triggered.connect(self.openSettings)
        menu.addAction("Exit", QApplication.instance().exit)

    def loadModel(self):
        def loadModelHelper(tracker):
            betterOCR = tracker.switchOCRMode()
            if betterOCR:
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
                    tracker.ocrModel = MangaOcr()
                return (betterOCR, connected)
            else:
                tracker.ocrModel = None
                return (betterOCR, True)

        def modelLoadedConfirmation(typeConnectionTuple):
            usingMangaOCR, connected = typeConnectionTuple
            modelName = "MangaOCR" if usingMangaOCR else "Tesseract"
            if connected:
                self.showMessage(
                    f"{modelName} model loaded",
                    f"You are now using the {modelName} model for Japanese text detection."
                )

            elif not connected:
                self.showMessage(
                    "Connection Error",
                    "Please try again or make sure your Internet connection is on."
                )

        self.showMessage(
            "Please wait",
            "Loading the MangaOCR model ..."
        )

        worker = BaseWorker(loadModelHelper, self.tracker)
        worker.signals.result.connect(modelLoadedConfirmation)
        self.threadpool.start(worker)

    def captureExternal(self):

        if self.tracker.ocrModel == None:
            self.showMessage(
                "MangaOCR model not yet loaded",
                "Please wait until the MangaOCR model is loaded."
            )
            return
        externalWindow = ExternalWindow(self.tracker)
        externalWindow.showFullScreen()

    # BUG: Menu is closing when some event in MangaOCR is triggered
    # Might be solvable using threads?
    def openSettings(self):
        SettingsMenu(self, self.tracker).show()

class SettingsMenu(QWidget):

    def __init__(self, parent=None, tracker=None):
        super(QWidget, self).__init__()
        self._parent = parent
        self.tracker = tracker
        self.config = parent.config

        self.vLayout = QVBoxLayout()
        self.ribbon = Ribbon(self, self.tracker)
        self.vLayout.addWidget(self.ribbon)
        self.setLayout(self.vLayout)

    # Save configurations on close
    def closeEvent(self, event):
        saveOnClose(self.config)
        self._parent.config = self.config
        return super().closeEvent(event)

    # Noop
    def poricomNoop(self):
        MessagePopup(
            "WIP",
            "This function is not yet implemented."
        ).exec()

# ------------------------------- Help Message ------------------------------- #

    def captureExternalHelper(self):
        self.showMinimized()
        sleep(0.5)
        if self.isMinimized():
            self._parent.captureExternal()

# ---------------------------------- Settings --------------------------------- #

    def modifyHotkeys(self):
        confirmation = PickerPopup(ShortcutPicker(self, self.tracker))
        ret = confirmation.exec()
        if ret:
            MessagePopup(
                "Shortcut Remapped",
                "Close the app to apply changes."
            ).exec()

    def modifyFontSettings(self):
        confirmation = PickerPopup(FontPicker(self, self.tracker))
        ret = confirmation.exec()

        if ret:
            app = QApplication.instance()
            if app is None:
                raise RuntimeError("No Qt Application found.")

            with open(config["STYLES_DEFAULT"], 'r') as fh:
                app.setStyleSheet(fh.read())

    def toggleLogging(self):
        self.tracker.switchWriteMode()
