"""
Cloe Constants

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

from PyQt5.QtGui import QColor, QFont

# General
APP_NAME = "Cloe"

# Images and styles
APP_LOGO = "./assets/images/icons/logo.ico"
STYLESHEET_LIGHT = "./assets/styles.qss"
STYLESHEET_DARK = "./assets/styles-dark.qss"
STYLESHEET_DEFAULT = "./assets/styles.qss"

# Settings
## Defaults
HOTKEYS_DEFAULT = {
    "startCapture": {
        "altKey": True,
        "mainKey": 17
    },
    "unmapped": {
        "shiftKey": False,
        "ctrlKey": False,
        "altKey": False,
        # "winKey": False,
        "mainKey": 0
    }
}
VIEW_SETTINGS_DEFAULT = {
    # Preview
    'previewFont': QFont("Arial", 16),
    'previewColor': QColor(239, 240, 241, 255),
    'previewBackground': QColor(72, 75, 106, 230),
    'previewPadding': 10,
    # Selection rubberband
    'selectionBorderColor': QColor(0, 128, 255, 255),
    'selectionBorderThickness': 2,
    'selectionBackground': QColor(0, 128, 255, 60),
    'windowColor': QColor(255, 255, 255, 13)
}
## Constants
UNMAPPED_KEY = "<Unmapped>"
VALID_KEY_LIST = [UNMAPPED_KEY, "A", "B", "C", "D", "E", "F", "G",
                 "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q",
                 "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

# Popups
ABOUT_MESSAGE = ("Inspired by <a href='http://capture2text.sourceforge.net/'>"
                "Capture2Text</a>, Cloe is a snipping tool for the "
                "<a href='https://pypi.org/project/manga-ocr'>MangaOCR library</a>."
                " The project works similarly to Capture2Text but uses the MangaOCR"
                " model instead.\n\n Acknowledgments:\n\n"
                "This project will not be possible without the MangaOCR model by "
                "<a href='https://github.com/kha-white'>Maciej Budyś</a>.\n"
                "The software is licensed under GPLv3 (see "
                "<a href='https://github.com/bluaxees/Cloe/blob/main/LICENSE'>"
                "LICENSE</a> and uses third party libraries that are distributed "
                "under their own terms (see <a href='"
                "https://github.com/bluaxees/Cloe/blob/main/LICENSE-3RD-PARTY'"
                "> LICENSE-3RD-PARTY</a>.\n The icons used in this project are made"
                " by <a href='https://icons8.com'> Icons8 </a>: "
                "<a href='https://icons8.com/icon/aPtgRkkLiNl2/settings'>settings</a>"
                ", <a href='https://icons8.com/icon/45/close'>close</a>, and "
                "<a href='https://icons8.com/icon/DHTiJWmR3fPx/about'>about</a>.")
