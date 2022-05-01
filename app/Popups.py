"""
Poricom Popup Components

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

from PyQt5.QtCore import (Qt)
from PyQt5.QtWidgets import (QGridLayout, QVBoxLayout, QWidget, QLabel, QPushButton, QApplication,
                             QLineEdit, QComboBox, QDialog, QDialogButtonBox, QMessageBox)

from utils.config import (editSelectionConfig, editStylesheet)


class MessagePopup(QMessageBox):
    def __init__(self, title, message, *args, **kwargs):
        super(QMessageBox, self).__init__(
            QMessageBox.NoIcon, title, message, *args, **kwargs)
        self.setAttribute(Qt.WA_DeleteOnClose)

    def addResetButtons(self):
        # BUG: This leaves a duplicate icon in the tray bar 
        def resetApplication():
            import os, sys
            QApplication.instance().quit()
            os.execl(sys.executable, sys.executable, *sys.argv)
        laterButton = QPushButton("Restart Later")
        nowButton = QPushButton("Restart Now")
        nowButton.clicked.connect(resetApplication)
        self.addButton(laterButton, QMessageBox.AcceptRole)
        self.addButton(nowButton, QMessageBox.AcceptRole)
