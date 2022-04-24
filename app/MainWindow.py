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
from PyQt5.QtCore import (Qt, QAbstractNativeEventFilter, QThreadPool)
from PyQt5.QtWidgets import (
    QVBoxLayout, QWidget, QMainWindow, QApplication)


from utils.config import config
from Workers import BaseWorker
from Ribbon import (Ribbon)
from Views import (FullScreen)
from Popups import (ShortcutPicker, FontPicker, PickerPopup, MessagePopup)


class WinEventFilter(QAbstractNativeEventFilter):
    def __init__(self, keybinder):
        self.keybinder = keybinder
        super().__init__()

    def nativeEventFilter(self, eventType, message):
        ret = self.keybinder.handler(eventType, message)
        return ret, 0


class ExternalWindow(QMainWindow):
    def __init__(self, tracker):
        super().__init__()
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet("border:0px; margin:0px")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        self.setCentralWidget(FullScreen(self, tracker))


class MainWindow(QMainWindow):

    def __init__(self, parent=None, tracker=None):
        super(QWidget, self).__init__(parent)
        self.tracker = tracker
        self.config = config

        self.vLayout = QVBoxLayout()
        self.ribbon = Ribbon(self, self.tracker)
        self.vLayout.addWidget(self.ribbon)
        _mainWidget = QWidget()
        _mainWidget.setLayout(self.vLayout)
        self.setCentralWidget(_mainWidget)

        self.threadpool = QThreadPool()

    # def closeEvent(self, event):
    #     try:
    #         rmtree("./poricom_cache")
    #     except FileNotFoundError:
    #         pass
    #     saveOnClose(self.config)
    #     return QMainWindow.closeEvent(self, event)

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
                MessagePopup(
                    f"{modelName} model loaded",
                    f"You are now using the {modelName} model for Japanese text detection."
                ).exec()

            elif not connected:
                MessagePopup(
                    "Connection Error",
                    "Please try again or make sure your Internet connection is on."
                ).exec()

        confirmation = MessagePopup(
            "Please wait",
            "Loading the MangaOCR model ..."
        )

        worker = BaseWorker(loadModelHelper, self.tracker)
        worker.signals.finished.connect(confirmation.close)
        worker.signals.result.connect(modelLoadedConfirmation)
        self.threadpool.start(worker)
        confirmation.exec()

    def poricomNoop(self):
        MessagePopup(
            "WIP",
            "This function is not yet implemented."
        ).exec()

# ------------------------------ Help Functions ------------------------------ #

    def captureExternalHelper(self):
        self.showMinimized()
        sleep(0.5)
        if self.isMinimized():
            self.captureExternal()

    def captureExternal(self):

        if self.tracker.ocrModel == None:
            MessagePopup(
            "MangaOCR model not yet loaded",
            "Please wait until the MangaOCR model is loaded."
            ).exec()
            return

        externalWindow = ExternalWindow(self.tracker)
        externalWindow.showFullScreen()

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
