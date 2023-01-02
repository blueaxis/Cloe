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

from typing import Any

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QCheckBox, QComboBox, QHBoxLayout, QLabel

from ..base import BaseSettings
from utils.constants import HOTKEYS_DEFAULT, UNMAPPED_KEY, VALID_KEY_LIST
from utils.scripts import camelizeText


class HotkeyContainer(BaseSettings):
    """Generic container for hotkey settings component

    Args:
        shortcutLabel (str): Text based on the name of the callable in the system tray application.
    """

    def __init__(self, shortcutLabel: str):
        self._shortcutName = camelizeText(shortcutLabel)
        super().__init__(None, "./utils/cloe-hotkey.ini", self._shortcutName)

        try:
            self._defaults = HOTKEYS_DEFAULT[self._shortcutName]
        except KeyError:
            self._defaults = HOTKEYS_DEFAULT["unmapped"]

        # Layout
        self.setLayout(QHBoxLayout(self))
        self.layout().setAlignment(Qt.AlignTop)
        margin = self.layout().contentsMargins()
        margin.setBottom(0)
        margin.setTop(7)
        self.layout().setContentsMargins(margin)

        self.initWidgets(shortcutLabel)
        self.loadSettings()

    # -------------------------------- UI Initializations -------------------------------- #

    def initWidgets(self, shortcutLabel: str):
        """
        Initialize checkboxes for the modifiers and combobox for the main key
        """
        self.shortcutLabel = QLabel(shortcutLabel)

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
        hotkey = self.getHotkeyText()
        if not hotkey:
            return self.loadSettings()
        hotkeys = self.settings.value("hotkeys", {}, type=dict)
        hotkeys[self._shortcutName] = hotkey
        self.settings.setValue("hotkeys", hotkeys)
        return super().saveSettings(hasMessage=False)

    # -------------------------------- Helpers Functions -------------------------------- #

    def getHotkeyText(self):
        """
        Computes hotkey combination text based on checkbox and combobox states
        """
        modifierText = ""
        for modifier in self.modifiers:
            if modifier.isChecked():
                modifierText += f"<{modifier.text()}>+"

        key = self.mainKey.currentText()
        if key == UNMAPPED_KEY:
            return ""
        modifierText += key
        return modifierText

    def getProperty(self, prop: str):
        # Overridden to handle checkbox and combobox
        obj = getattr(self, prop)
        if isinstance(obj, QCheckBox):
            return obj.isChecked()
        elif isinstance(obj, QComboBox):
            return obj.currentIndex()
        return super().getProperty(prop)

    def setProperty(self, prop: str, value: Any):
        # Overridden to handle checkbox and combobox
        obj = getattr(self, prop)
        if isinstance(obj, QCheckBox):
            return obj.setChecked(value.lower() == "true")
        elif isinstance(obj, QComboBox):
            return obj.setCurrentIndex(int(value))
        return super().setProperty(prop, value)
