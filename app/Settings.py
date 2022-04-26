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


from PyQt5.QtGui import (QColor, QPalette, QBrush, QPainter, QPen)
from PyQt5.QtCore import (Qt, QSize, QSettings)
from PyQt5.QtWidgets import (QComboBox, QLineEdit, QLabel, QInputDialog, QColorDialog, 
    QRubberBand, QApplication, QGridLayout, QHBoxLayout, QWidget, QTabWidget, QPushButton, QVBoxLayout)

class CustomBand(QRubberBand):

    def __init__(self, shape, parent, color=Qt.blue, thickness=2):
        super().__init__(shape, parent)
        self.setBorder(color, thickness)
    
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
        self.settings = QSettings("./utils/MangaOCR.ini", QSettings.IniFormat)

        # Properties and defaults
        self._defaults = {
            # Preview
            'previewFont': 'font',
            'previewColor': "rgba(239, 240, 241, 1)",
            'previewBackground': "rgba(72, 75, 106, 0.9)",
            'previewPadding': "0.25em",

            # Selection rubberband
            'selectionBorderColor': QColor(0, 128, 255, 60),
            'selectionBorderThickness': 2,
            'selectionBackground': QColor(0, 128, 255, 255),
            'windowColor': "rgba(255, 255, 255, 0.01)"
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

        self.setLayout(QGridLayout(self))
        # self.layout().setContentsMargins(0, 0, 0, 0)
        self.initSettings()
        self.initButtons()
        self.initLiveView()
        self.updateLiveView()

    def resizeEvent(self, event):
        # Resize rubber band when window size is changed
        w = 0.35 * self._liveView.width() 
        y = 0.05 * self._liveView.height()
        x = self._liveView.width() - w - y
        h = self._liveView.height() - 2*y
        self._rubberBand.setGeometry(x, y, w, h)
        return super().resizeEvent(event)

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
        _windowColor.clicked.connect(lambda: self.getColor_('windowColor'))

    def initLiveView(self):
        # Live View
        self._liveView = QWidget()
        self._liveView.setObjectName('liveView')
        self._liveView.setLayout(QGridLayout(self._liveView))

        # Selection Rubberband Live View
        self._rubberBand = CustomBand(QRubberBand.Rectangle, self._liveView)
        self._rubberBand.setObjectName('selectionBand')
        
        # Preview Text Live View
        self._previewText = QLabel(" Sample Text ")
        self._previewText.setObjectName('previewText')
        self._previewText.adjustSize()
        self._liveView.layout().addWidget(self._previewText, 0, 0, alignment=Qt.AlignTop | Qt.AlignLeft)
        self._rubberBand.show()
        self.layout().addWidget(self._liveView, 2, 0, -1, -1)

    def initSettings(self):
        for propName, propType in self._properties.items():
            try:
                if propType == 'rgba':
                    _c = self.settings.value(propName)
                    prop = f"rgba({_c.red()}, {_c.green()}, {_c.blue()}, {_c.alpha()})"
                elif propType == 'color':
                    prop = self.settings.value(propName)
                elif propType == 'dist':
                    pass
                elif propType == 'font':
                    pass
                if prop is not None: setattr(self, propName, self._defaults[propName])
                else: raise TypeError
            except:
                setattr(self, propName, self._defaults[propName])

    def updateLiveView(self):
        self.previewPadding = '0.25em'
        self.selectionBorderThickness = '0.1em'
        styles = f"""
            QLabel#previewText {{ 
                color: {self.previewColor};
                background-color: {self.previewBackground}; 
                padding: {self.previewPadding};
                font-family: 'Helvetica';
                font-size: 16pt;
                margin-top: 0.02em;
                margin-left: 0.02em;
            }}
            """
        self.setStyleSheet(styles)

        palette = QPalette()
        palette.setBrush(QPalette.Highlight, QBrush(self.selectionBackground))
        self._rubberBand.setBorder(self.selectionBorderColor, 2)
        self._rubberBand.setPalette(palette) 
   
    def getColor_(self, objectName):
        try:
            initialColor = self.settings.value(objectName)
        except:
            pass
        if initialColor is None:
            initialColor = QColor()
        _c = QColorDialog().getColor(initial=initialColor, options=QColorDialog.ShowAlphaChannel)
        if _c.isValid():
            self.settings.setValue(objectName, _c)
            if self._properties[objectName] == 'rgba':
                color = f"rgba({_c.red()}, {_c.green()}, {_c.blue()}, {_c.alpha()})"
                setattr(self, objectName, color)
            else: setattr(self, objectName, _c)
            self.updateLiveView()

class SettingsMenu(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.tabs = QTabWidget()
        self.tabs.addTab(ViewSettings(), "VIEW")
        self.tabs.addTab(ViewSettings(), "VIEW")

        self.setLayout(QVBoxLayout(self))
        self.layout().addWidget(self.tabs)
        self.setMinimumSize(600, 400)

