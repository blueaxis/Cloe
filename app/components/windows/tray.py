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

from manga_ocr import MangaOcr
from PyQt5.QtCore import QObject, QSettings, QThreadPool
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMenu, QSystemTrayIcon

from .external import ExternalWindow
from components.popups import AboutPopup
from components.services import BaseWorker, Hotkeys
from components.settings import SettingsMenu
from utils.constants import (
    ABOUT_ICON,
    APP_LOGO,
    EXIT_ICON,
    HOTKEY_CONFIG,
    SETTINGS_ICON,
)


class SystemTray(QSystemTrayIcon):
    """
    System tray application containing all global actions
    """

    def __init__(self, parent=None):
        super().__init__(QIcon(APP_LOGO), parent)

        # State trackers and configurations
        self.threadpool = QThreadPool()
        self.ocrModel: MangaOcr = None
        self.loadHotkeys()

        # Menu
        menu = QMenu(parent)
        self.setContextMenu(menu)

        # Menu Actions
        menu.addAction(QIcon(SETTINGS_ICON), "Settings", self.openSettings)
        menu.addSeparator()
        menu.addAction(QIcon(ABOUT_ICON), "About Chloe", self.openAbout)
        menu.addAction(QIcon(EXIT_ICON), "Exit", self.closeApplication)

        self.externalWindow = None
        self.settingsMenu = None

    def processGlobalHotkey(self, objectMethod: tuple[QObject, str]):
        obj, fn = objectMethod
        getattr(obj, fn)()

    def loadHotkeys(self):
        try:
            self.hotkeys.stop()
        except Exception:
            pass
        self.hotkeys = Hotkeys(self.getHotkeys())
        self.hotkeys.start()
        self.hotkeys.signals.result.connect(self.processGlobalHotkey)

    def getHotkeys(self):
        hotkeyDict = {}
        hotkeySettings = QSettings(HOTKEY_CONFIG, QSettings.IniFormat)
        hotkeys = hotkeySettings.value("hotkeys")
        if hotkeys:
            for action, hotkey in hotkeys.items():
                if hotkey:
                    hotkeyDict[hotkey] = (self, action)
        elif not hotkeys:
            hotkeyDict["<Alt>+Q"] = (self, "startCapture")
        return hotkeyDict

    def loadModel(self):
        def loadModelHelper():
            try:
                self.showMessage("Please wait", "Loading the MangaOCR model ...")
                self.ocrModel = MangaOcr()
                return "success"
            except Exception as e:
                return str(e)

        def loadModelConfirm(message: str):
            if message.lower() == "success":
                self.showMessage(
                    "MangaOCR model loaded",
                    "You are now using the MangaOCR model for Japanese text detection.",
                )
            else:
                self.showMessage("Load Model Error", message)

        worker = BaseWorker(loadModelHelper)
        worker.signals.result.connect(loadModelConfirm)
        self.threadpool.start(worker)

    def startCapture(self):
        if self.ocrModel == None:
            self.showMessage(
                "MangaOCR model not yet loaded",
                "Please wait until the MangaOCR model is loaded.",
            )
            return
        if self.externalWindow is None:
            self.externalWindow = ExternalWindow(self)
        if not self.externalWindow.isVisible():
            self.externalWindow.showFullScreen()

    def openSettings(self):
        if self.settingsMenu is None:
            self.settingsMenu = SettingsMenu(self)
        self.settingsMenu.show()

    def openAbout(self):
        AboutPopup().exec()

    def closeApplication(self):
        QApplication.instance().exit()
