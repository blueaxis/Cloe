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
from PyQt5.QtWidgets import (
    QGridLayout,
    QLabel,
    QPushButton,
    QWidget,
    QInputDialog,
    QColorDialog,
    QFontDialog,
)

from ..tab import BaseSettingsTab
from .container import ViewContainer
from .preview import Preview


class ViewSettingsTab(ViewContainer, BaseSettingsTab):
    """
    Settings tab for view-related settings
    """

    def __init__(self, parent: QWidget):

        super().__init__(parent, "./utils/cloe-view.ini")

        self.setLayout(QGridLayout(self))
        self.initButtons()
        self.initPreview()
        self.updateViewStyles()
        self.addButtonBar(self.layout().rowCount())

    # ------------------------------ UI Initializations ----------------------------- #

    def initButtons(self):
        """
        Initialize controls for the preview
        """

        # ------------------------------- Preview Text ------------------------------ #

        # Button Initializations
        _previewTitle = QLabel("Preview ")
        _previewFont = QPushButton("Font Style")
        _previewColor = QPushButton("Font Color")
        _previewBackground = QPushButton("Background Color")
        _previewPadding = QPushButton("Padding")

        # Layout
        self.layout().addWidget(_previewTitle, 0, 0, 1, 1)
        self.layout().addWidget(_previewFont, 0, 1, 1, 2)
        self.layout().addWidget(_previewColor, 0, 3, 1, 2)
        self.layout().addWidget(_previewBackground, 0, 5, 1, 2)
        self.layout().addWidget(_previewPadding, 0, 7, 1, 2)

        # Signals and Slots
        _previewColor.clicked.connect(lambda: self.getColor("previewColor"))
        _previewBackground.clicked.connect(lambda: self.getColor("previewBackground"))
        _previewFont.clicked.connect(lambda: self.getFont("previewFont"))
        _previewPadding.clicked.connect(lambda: self.getInt("previewPadding"))

        # --------------------------- Selection Rubberband -------------------------- #

        # Button Initializations
        _selectionTitle = QLabel("Selection ")
        _selectionBorderColor = QPushButton("Border Color")
        _selectionBorderThickness = QPushButton("Border Thickness")
        _selectionBackground = QPushButton("Mask Color")
        _windowColor = QPushButton("Window Color")

        # Layout
        self.layout().addWidget(_selectionTitle, 1, 0, 1, 1)
        self.layout().addWidget(_selectionBorderColor, 1, 1, 1, 2)
        self.layout().addWidget(_selectionBorderThickness, 1, 3, 1, 2)
        self.layout().addWidget(_selectionBackground, 1, 5, 1, 2)
        self.layout().addWidget(_windowColor, 1, 7, 1, 2)

        # Signals and Slots
        _selectionBorderColor.clicked.connect(
            lambda: self.getColor("selectionBorderColor")
        )
        _selectionBackground.clicked.connect(
            lambda: self.getColor("selectionBackground")
        )
        _selectionBorderThickness.clicked.connect(
            lambda: self.getInt("selectionBorderThickness")
        )
        _windowColor.clicked.connect(lambda: self.getColor("windowColor"))

    def initPreview(self):
        self._preview = Preview(self)
        self.layout().addWidget(self._preview, 2, 0, 1, -1)
        self.layout().setRowStretch(self.layout().rowCount() - 1, 1)

    # ----------------------------------- Settings ---------------------------------- #

    def resetSettings(self):
        # Overridden to update styles on reset
        super().resetSettings()
        self.updateViewStyles()

    # ------------------------- Property Setters and Getters ------------------------ #

    def setPropertyAndUpdate(self, prop: str, value: Any):
        super().setProperty(prop, value)
        self.updateViewStyles()

    def getColor(self, prop: str):
        initial = self.getProperty(prop)
        color = QColorDialog(self).getColor(
            initial=initial, options=QColorDialog.ShowAlphaChannel
        )
        if color.isValid():
            self.setPropertyAndUpdate(prop, color)

    def getFont(self, prop: str):
        initial = self.getProperty(prop)
        font, accepted = QFontDialog(self).getFont(initial)
        if accepted:
            self.setPropertyAndUpdate(prop, font)

    def getInt(self, prop: str, minimum=1, maximum=50):
        initial = self.getProperty(prop)
        i, accepted = QInputDialog.getInt(
            self,
            "Margin/Padding Settings",
            f"Enter a value between {minimum} and {maximum}:",
            value=initial,
            min=minimum,
            max=maximum,
            flags=Qt.CustomizeWindowHint | Qt.WindowTitleHint,
        )
        if accepted:
            self.setPropertyAndUpdate(prop, i)
