"""
Cloe View Settings Tab

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

from typing import Optional

from PyQt5.QtCore import (QSettings)
from PyQt5.QtGui import (QColor, QFont)
from PyQt5.QtWidgets import (QWidget)

from utils.constants import VIEW_SETTINGS_DEFAULT
from utils.scripts import colorToRGBA


class ViewContainer(QWidget):
    """
    Generic view container
    """
    def __init__(self, parent: QWidget):
        super().__init__(parent)

        self.loadSettings()

# ------------------------------------- Settings ------------------------------------- #

    def loadSettings(self, file="./utils/cloe-view.ini"):
        """Load the settings from the configuration file

        Args:
            file (str, optional): Path to configuration file.
            Defaults to "./utils/cloe-view.ini".
        """
        self.settings = QSettings(file, QSettings.IniFormat)
        # Default settings if not provided by config
        self._defaults = VIEW_SETTINGS_DEFAULT
        for propName, propDefault in self._defaults.items():
            prop = self.settings.value(propName, propDefault)
            if isinstance(prop, str):
                prop = int(prop)
            setattr(self, propName, prop)

# ----------------------------------- View Updates ----------------------------------- #

    def getPreviewTextStyles(self, font: QFont, padding:int, color: QColor, background: QColor):
        """Converts parameters to QSS styles for the previewText

        Args:
            font (QFont): Font of the preview text.
            padding (int): Padding of the preview box.
            color (QColor): Color of the preview text.
            background (QColor): Background color of the preview box.
        """
        styles = f"""
            QLabel#previewText {{ 
                color: {color};
                background-color: {background}; 
                padding: {padding}px;
                font-family: {font.family()};
                font-size: {font.pointSize()}pt;
                margin-top: 0.02em;
                margin-left: 0.02em;
            }}\n
        """
        return styles

    def updateViewStyles(self, view: Optional[QWidget] = None):
        """Sets the style of the view

        Args:
            view (QWidget, optional): The view to be updated. Defaults to None.
        """
        # Update preview text style
        styles = self.getPreviewTextStyles(self.previewFont, self.previewPadding,
            colorToRGBA(self.previewColor), colorToRGBA(self.previewBackground))

        if not view:
            try:
                view = self._preview
            except AttributeError:
                return

        view.parentWidget().setStyleSheet(styles)
        view.rubberBand.setFill(self.selectionBackground)
        view.rubberBand.setBorder(self.selectionBorderColor, self.selectionBorderThickness)
        view.setBackgroundColor(self.windowColor)
