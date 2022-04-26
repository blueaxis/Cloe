"""
Poricom Settings Menu Components

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

from PyQt5.QtGui import (QColor, QPalette, QBrush, QPainter, QPen, QFont)
from PyQt5.QtCore import (Qt, QSize, QSettings)
from PyQt5.QtWidgets import (QComboBox, QLineEdit, QLabel, QInputDialog, QColorDialog, QFontDialog,
    QRubberBand, QApplication, QGridLayout, QHBoxLayout, QWidget, QTabWidget, QPushButton, QVBoxLayout)

class CustomBand(QRubberBand):

    def __init__(self, shape, parent, borderColor=Qt.blue, thickness=2):
        super().__init__(shape, parent)
        self.setBorder(borderColor, thickness)
    
    def setBorder(self, color, thickness):
        self._borderColor = color
        self._borderThickness = thickness

    def paintEvent(self, event):
        painter = QPainter()
        pen = QPen(self._borderColor, self._borderThickness)
        pen.setStyle(Qt.SolidLine)
        painter.begin(self)
        painter.setPen(pen)
        painter.drawRect(event.rect())
        painter.end()
        return super().paintEvent(event)

class ViewSettings(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

        self.setLayout(QGridLayout(self))
        self.restoreSettings()
        self.initButtons()
        self.initLiveView()
        self.updateLiveView()

# ----------------------------------- View Updates ----------------------------------- #

    def resizeEvent(self, event):
        if self._liveView is not None:
            # Resize rubber band when window size is changed
            w = 0.35 * self._liveView.width() 
            y = 0.05 * self._liveView.height()
            x = self._liveView.width() - w - y
            h = self._liveView.height() - 2*y
            self._rubberBand.setGeometry(x, y, w, h)
        return super().resizeEvent(event)

    def updateLiveView(self):

        def colorToRGBA(objectName):
            _c = getattr(self, objectName)
            if self._properties[objectName] == 'rgba':
                color = f"rgba({_c.red()}, {_c.green()}, {_c.blue()}, {_c.alpha()})"
                return color

        _previewPadding = f"{self.previewPadding}px"
        _previewColor = colorToRGBA('previewColor')
        _previewBackground = colorToRGBA('previewBackground')
        # TODO: Window color is not set properly since parent color is different
        # BUG: Styles are not being applied to liveView object
        _windowColor = colorToRGBA('windowColor')
        styles = f"""
            QLabel#previewText {{ 
                color: {_previewColor};
                background-color: {_previewBackground}; 
                padding: {_previewPadding};
                font-family: {self.previewFont.family()};
                font-size: {self.previewFont.pointSize()}pt;
                margin-top: 0.02em;
                margin-left: 0.02em;
            }}
        """
        self.setStyleSheet(styles)

        # BUG: Rubberband not updating on start
        palette = QPalette()
        palette.setBrush(QPalette.Highlight, QBrush(self.selectionBackground))
        self._rubberBand.setPalette(palette)
        self._rubberBand.setBorder(self.selectionBorderColor, self.selectionBorderThickness)

# --------------------------- Settings and Initializations --------------------------- #

    def restoreSettings(self):
        self.settings = QSettings("./utils/MangaOCR.ini", QSettings.IniFormat)
        # Properties and defaults
        self._defaults = {
            # Preview
            'previewFont': QFont("Arial", 16),
            'previewColor': QColor(239, 240, 241, 255),
            'previewBackground': QColor(72, 75, 106, 230),
            'previewPadding': 10,
            # Selection rubberband
            'selectionBorderColor': QColor(0, 128, 255, 60),
            'selectionBorderThickness': 2,
            'selectionBackground': QColor(0, 128, 255, 255),
            'windowColor': QColor(255, 255, 255, 3)
        }
        self._properties = {
            # Preview
            'previewFont': 'font',
            'previewColor': 'rgba',
            'previewBackground': 'rgba',
            'previewPadding': 'dist',
            # Selection rubberband
            'selectionBorderColor': 'color',
            'selectionBorderThickness': 'dist',
            'selectionBackground': 'color',
            'windowColor': 'rgba'
        }
        for propName, propType in self._properties.items():
            try:
                if propType == 'rgba':
                    prop = self.settings.value(propName)
                elif propType == 'color':
                    prop = self.settings.value(propName)
                elif propType == 'dist':
                    prop = int(self.settings.value(propName))
                elif propType == 'font':
                    prop = self.settings.value(propName)
                if prop is not None:
                    setattr(self, propName, prop)
                    self.settings.setValue(propName, prop)
                else: raise TypeError
            except:
                setattr(self, propName, self._defaults[propName])
                self.settings.setValue(propName, self._defaults[propName])
        return self.settings, self._properties

    def initButtons(self):

        # ------------------------------- Preview Text ------------------------------- #

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
        _previewColor.clicked.connect(lambda: self.getColor_('previewColor'))        
        _previewBackground.clicked.connect(lambda: self.getColor_('previewBackground'))
        _previewFont.clicked.connect(lambda: self.getFont_('previewFont'))
        _previewPadding.clicked.connect(lambda: self.getInt_('previewPadding'))

        # --------------------------- Selection Rubberband --------------------------- #        
# --------------------------- Selection Rubberband --------------------------- #        
        # --------------------------- Selection Rubberband --------------------------- #        

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
        _selectionBorderColor.clicked.connect(lambda: self.getColor_('selectionBorderColor'))
        _selectionBackground.clicked.connect(lambda: self.getColor_('selectionBackground'))
        _selectionBorderThickness.clicked.connect(lambda: self.getInt_('selectionBorderThickness'))
        _windowColor.clicked.connect(lambda: self.getColor_('windowColor'))

    def initLiveView(self):
        # Live View
        self._liveView = QWidget()
        self._liveView.setObjectName('liveView')
        self._liveView.setLayout(QGridLayout(self._liveView))

        # Selection Rubberband Live View
        self._rubberBand = CustomBand(CustomBand.Rectangle, self._liveView)
        self._rubberBand.setObjectName('selectionBand')
        
        # Preview Text Live View
        self._previewText = QLabel(" Sample Text ")
        self._previewText.setObjectName('previewText')
        self._previewText.adjustSize()
        self._liveView.layout().addWidget(self._previewText, 0, 0, alignment=Qt.AlignTop | Qt.AlignLeft)
        self._rubberBand.show()
        self.layout().addWidget(self._liveView, 2, 0, -1, -1)

# --------------------------- Property Setters and Getters --------------------------- #

    def setProperty_(self, objectName, value):
        self.settings.setValue(objectName, value)
        setattr(self, objectName, value)
        self.updateLiveView()

    def getColor_(self, objectName):
        try:
            initialColor = self.settings.value(objectName)
        except:
            initialColor = None
        if initialColor is None:
            initialColor = self._defaults[objectName]
        color = QColorDialog().getColor(initial=initialColor, options=QColorDialog.ShowAlphaChannel)
        if color.isValid():
            self.setProperty_(objectName, color)

    def getFont_(self, objectName):
        try:
            initialFont = self.settings.value(objectName)
        except:
            initialFont = None
        if initialFont is None:
            initialFont = self._defaults[objectName]
        font, accepted = QFontDialog().getFont(initialFont)
        if accepted:
            self.setProperty_(objectName, font)

    def getInt_(self, objectName):
        try:
            initialInt = int(self.settings.value(objectName))
        except:
            initialInt = None
        if initialInt is None:
            initialInt = self._defaults[objectName]
        i, accepted = QInputDialog.getInt(
            self,
            "Margin/Padding Settings",
            f"Enter a value between 5 and 50:",
            value=initialInt,
            min=5,
            max=50,
            flags=Qt.CustomizeWindowHint | Qt.WindowTitleHint)

        if accepted:
            self.setProperty_(objectName, i)


class SettingsMenu(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.tabs = QTabWidget()
        self.tabs.addTab(ViewSettings(), "VIEW")
        self.tabs.addTab(ViewSettings(), "VIEW")

        self.setLayout(QVBoxLayout(self))
        self.layout().addWidget(self.tabs)
        self.setMinimumSize(600, 400)

