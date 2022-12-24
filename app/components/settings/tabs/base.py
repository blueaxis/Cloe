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

from os import remove

from PyQt5.QtCore import Qt, QSettings
from PyQt5.QtWidgets import QHBoxLayout, QPushButton, QWidget

# TODO: Settings UI and settings core should be different classes
class BaseSettingsTab(QWidget):
    """Base settings tab to allow saving/loading settings

    Args:
        parent (QWidget): Parent widget. Set to SettingsMenu object.
    """

    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.settings: QSettings = None

    # -------------------------------- UI Initializations -------------------------------- #

    def addButtonBar(self, row: int):
        """
        Creates a button bar at the bottom of the tab
        """
        buttonBar = QWidget()
        buttonBar.setLayout(QHBoxLayout(buttonBar))
        buttonBar.layout().setContentsMargins(0, 0, 0, 0)

        self.okButton = QPushButton("Save")
        self.cancelButton = QPushButton("Close")
        self.defaultButton = QPushButton("Restore Defaults")

        self.okButton.clicked.connect(self.saveSettings)
        self.cancelButton.clicked.connect(self.parent().close)
        self.defaultButton.clicked.connect(self.restoreDefaultSettings)

        buttonBar.layout().addWidget(self.defaultButton)
        buttonBar.layout().addStretch()
        buttonBar.layout().addWidget(self.okButton)
        buttonBar.layout().addWidget(self.cancelButton)

        self.layout().addWidget(buttonBar, row, 0, 1, -1, alignment=Qt.AlignBottom)

    # ------------------------------------- Settings ------------------------------------- #

    def saveSettings(self):
        pass

    def reloadSettings(self):
        self.loadSettings()

    # TODO: Add confirm before restoring defaults
    def restoreDefaultSettings(self):
        try:
            remove(self.settings.fileName())
        except FileNotFoundError:
            pass
        self.reloadSettings()
