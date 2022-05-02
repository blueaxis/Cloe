"""
Cloe Popup Components

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
from PyQt5.QtWidgets import (QApplication, QPushButton, QMessageBox)


class MessagePopup(QMessageBox):
    def __init__(self, title, message, *args, **kwargs):
        super(QMessageBox, self).__init__(
            QMessageBox.NoIcon, title, message, *args, **kwargs)
        self.setAttribute(Qt.WA_DeleteOnClose)

    def addResetButtons(self):
        # BUG: This leaves a duplicate icon in the tray bar
        def resetApplication():
            import os
            import sys
            QApplication.instance().quit()
            os.execl(sys.executable, sys.executable, *sys.argv)
        laterButton = QPushButton("Restart Later")
        nowButton = QPushButton("Restart Now")
        nowButton.clicked.connect(resetApplication)
        self.addButton(laterButton, QMessageBox.AcceptRole)
        self.addButton(nowButton, QMessageBox.AcceptRole)


class AboutPage(QMessageBox):
    def __init__(self):
        title = "About Cloe"
        message = ("Inspired by <a href='http://capture2text.sourceforge.net/'>"
                   "Capture2Text</a>, Cloe is a snipping tool for the "
                   "<a href='https://pypi.org/project/manga-ocr'>MangaOCR library</a>."
                   " The project works similarly to Capture2Text but uses the MangaOCR"
                   " model instead.\n\n Acknowledgments:\n\n"
                   "This project will not be possible without the MangaOCR model by "
                   "<a href='https://github.com/kha-white'>Maciej Budyś</a>.\n"
                   "The software is licensed under GPLv3 (see "
                   "<a href='https://github.com/bluaxees/Manga2OCR/blob/main/LICENSE'>"
                   "LICENSE</a> and uses third party libraries that are distributed "
                   "under their own terms (see <a href='"
                   "https://github.com/bluaxees/Manga2OCR/blob/main/LICENSE-3RD-PARTY'"
                   "> LICENSE-3RD-PARTY</a>.\n The icons used in this project are made"
                   " by <a href='https://icons8.com'> Icons8 </a>: "
                   "<a href='https://icons8.com/icon/aPtgRkkLiNl2/settings'>settings</a>"
                   ", <a href='https://icons8.com/icon/45/close'>close</a>, and "
                   "<a href='https://icons8.com/icon/DHTiJWmR3fPx/about'>about</a>.")
        super(QMessageBox, self).__init__(
            QMessageBox.NoIcon, title, message, QMessageBox.Ok)
        self.setAttribute(Qt.WA_DeleteOnClose)