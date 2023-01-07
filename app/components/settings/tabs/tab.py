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

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QPushButton, QWidget

from .base import BaseSettings


class BaseSettingsTab(BaseSettings):
    """Base settings tab that connects core settings functions to UI elements

    Args:
        parent (QWidget): Parent widget. Set to SettingsMenu object.
    """

    def __init__(self, parent: QWidget, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        # Manually set menu since QTabWidget children is reparented
        self.menu = parent

    def addButtonBar(self, row: int):
        """
        Creates a button bar at the bottom of the tab
        """
        buttonBar = QWidget()
        buttonBar.setLayout(QHBoxLayout(buttonBar))
        buttonBar.layout().setContentsMargins(0, 0, 0, 0)

        self.saveButton = QPushButton("Save")
        self.closeButton = QPushButton("Close")
        self.resetButton = QPushButton("Restore Defaults")

        self.saveButton.clicked.connect(lambda: self.saveSettings())
        self.closeButton.clicked.connect(self.menu.close)
        self.resetButton.clicked.connect(self.confirmResetSettings)

        buttonBar.layout().addWidget(self.resetButton)
        buttonBar.layout().addStretch()
        buttonBar.layout().addWidget(self.saveButton)
        buttonBar.layout().addWidget(self.closeButton)

        self.layout().addWidget(buttonBar, row, 0, 1, -1, alignment=Qt.AlignBottom)
