"""
Cloe Settings Tab Components

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

from PyQt5.QtCore import Qt, QSettings
from PyQt5.QtWidgets import QGridLayout, QWidget

from ..base import BaseSettingsTab
from .container import HotkeyContainer
from components.popups import BasePopup


class HotkeySettingsTab(BaseSettingsTab):
    """
    Settings tab for hotkey-related settings
    """

    def __init__(self, parent: QWidget):
        super().__init__(parent)
        # TODO: SettingsMenu is not being set as parent
        self.menu = parent
        self.settings = QSettings("./utils/cloe-hotkey.ini", QSettings.IniFormat)

        # Layout and margins
        self.setLayout(QGridLayout(self))
        self.layout().setAlignment(Qt.AlignTop)

        self.initializeHotkeyContainers()
        self.layout().addWidget(QWidget())
        self.layout().setRowStretch(self.layout().rowCount() - 1, 1)
        self.addButtonBar(self.layout().rowCount())

    # -------------------------------- UI Initializations -------------------------------- #

    def initializeHotkeyContainers(self):
        """Initialize HotkeyContainer widgets for the given actions

        *Note: The action must be a callable name in the system tray app
        (converted to TitleCase separated by whitespace).
        """

        self.containers = []
        actions = ["Start Capture", "Open Settings", "Close Application"]
        for action in actions:
            self.containers.append(HotkeyContainer(action))
            self.layout().addWidget(self.containers[-1])

    # ------------------------------------- Settings ------------------------------------- #

    def saveSettings(self):
        hotkeys = {}
        for container in self.containers:
            hotkey, action = container.saveSettings()
            hotkeys[action] = hotkey
        # TODO: Save config in HotkeyContainer instead
        self.settings.setValue("hotkeys", hotkeys)
        message = BasePopup("Configuration Saved", "New shortcuts have been applied.")
        message.exec()
        self.menu.onSaveHotkeys()

    def loadSettings(self):
        for container in self.containers:
            container.loadSettings()
