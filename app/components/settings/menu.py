"""
Cloe Settings Menu Component

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

from PyQt5.QtWidgets import QVBoxLayout, QWidget, QTabWidget

from .tabs import ViewSettingsTab, HotkeySettingsTab


class SettingsMenu(QWidget):
    """
    Container of the settings tabs
    """

    def __init__(self, parent):
        super().__init__()
        # Manually set system tray since QSystemTrayIcon is not a QWidget
        self.systemTray = parent

        self.tabs = QTabWidget()
        self.tabs.addTab(HotkeySettingsTab(self), "HOTKEYS")
        self.tabs.addTab(ViewSettingsTab(self), "VIEW")

        self.setLayout(QVBoxLayout(self))
        self.layout().addWidget(self.tabs)
        self.setFixedSize(625, 400)

    def onSaveHotkeys(self):
        self.systemTray.loadHotkeys()
