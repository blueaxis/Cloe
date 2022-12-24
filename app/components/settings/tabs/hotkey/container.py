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

from typing import Union

from PyQt5.QtCore import Qt, QSettings
from PyQt5.QtWidgets import QHBoxLayout, QWidget, QLabel, QComboBox, QCheckBox

from utils.constants import HOTKEYS_DEFAULT, UNMAPPED_KEY, VALID_KEY_LIST
from utils.scripts import camelizeText


class HotkeyContainer(QWidget):
    """Generic container for hotkey settings component

    Args:
        shortcutName (str): Name of the shortcut.
        Based on the name of the callable in the system tray application.
    """

    def __init__(self, shortcutName: str):
        super().__init__()

        # Layout
        self.setLayout(QHBoxLayout(self))
        self.layout().setAlignment(Qt.AlignTop)
        margin = self.layout().contentsMargins()
        margin.setBottom(0)
        margin.setTop(7)
        self.layout().setContentsMargins(margin)

        self.initWidgets(shortcutName)
        self.loadSettings()

    # -------------------------------- UI Initializations -------------------------------- #

    def initWidgets(self, shortcutName: str):
        """
        Initialize checkboxes for the modifiers and combobox for the main key
        """
        self.shortcutLabel = QLabel(shortcutName)

        # Modifiers
        self.shiftKey = QCheckBox("Shift")
        self.ctrlKey = QCheckBox("Ctrl")
        self.altKey = QCheckBox("Alt")
        # self.winKey = QCheckBox("Win")
        self.modifiers = [
            self.shiftKey,
            self.ctrlKey,
            self.altKey,
            # self.winKey,
        ]

        # Key
        self.mainKey = QComboBox()
        self.mainKey.addItems(VALID_KEY_LIST)

        # Layout
        self.layout().addWidget(self.shortcutLabel, alignment=Qt.AlignLeft)
        self.layout().addStretch()
        for modifier in self.modifiers:
            self.layout().addWidget(modifier, alignment=Qt.AlignRight)
        self.layout().addWidget(self.mainKey, alignment=Qt.AlignRight)

    # ------------------------------------- Settings ------------------------------------- #

    def saveSettings(self):
        """
        Save configuration based on current widget states
        """
        modifierText = ""
        for modifier in self.modifiers:
            if modifier.isChecked():
                modifierText += f"<{modifier.text()}>+"

        key = self.mainKey.currentText()
        # TODO: Do not save hotkey if unmapped
        if key == UNMAPPED_KEY:
            key = ""
        modifierText += key

        shortcutName = camelizeText(self.shortcutLabel.text())
        self.settings.setValue(shortcutName, self.getContainerState())
        return modifierText, shortcutName

    def loadSettings(self, file="./utils/cloe-hotkey.ini"):
        """Load the settings from the configuration file

        Args:
            file (str, optional): Path to configuration file.
            Defaults to "./utils/cloe-hotkey.ini".
        """
        self.settings = QSettings(file, QSettings.IniFormat)

        # Properties and defaults
        shortcutName = camelizeText(self.shortcutLabel.text())
        try:
            self._defaults = HOTKEYS_DEFAULT[shortcutName]
        except KeyError:
            self._defaults = HOTKEYS_DEFAULT["unmapped"]

        shortcut = self.settings.value(shortcutName, self._defaults, type=dict)
        for propName, propDefault in shortcut.items():
            self.setWidgetState(propName, propDefault)

    # -------------------------------- Helpers Functions -------------------------------- #

    def getContainerState(self):
        state = {}
        for propName, _ in self._defaults.items():
            state[propName] = self.getWidgetState(propName)
        return state

    def getWidgetState(self, objectName: str):
        obj = getattr(self, objectName)
        if isinstance(obj, QCheckBox):
            return obj.isChecked()
        elif isinstance(obj, QComboBox):
            return obj.currentIndex()

    def setWidgetState(self, objectName: str, objectState: Union[bool, int] = 0):
        obj = getattr(self, objectName)
        if isinstance(obj, QCheckBox):
            obj.setChecked(objectState)
        elif isinstance(obj, QComboBox):
            obj.setCurrentIndex(objectState)
