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

from os import remove

from PyQt5.QtGui import (QColor, QPalette, QBrush, QPainter, QPen, QFont)
from PyQt5.QtCore import (Qt, QSize, QSettings)
from PyQt5.QtWidgets import (QComboBox, QLineEdit, QLabel, QInputDialog, QColorDialog, QFontDialog,
    QRubberBand, QCheckBox, QGridLayout, QHBoxLayout, QWidget, QTabWidget, QPushButton, QVBoxLayout)

from Preview import PreviewContainer

class SettingsTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

    def addButtonBar(self, row):
        buttonBar = QWidget()
        buttonBar.setLayout(QHBoxLayout(buttonBar))
        buttonBar.layout().setContentsMargins(0, 0, 0, 0)

        self.okButton = QPushButton("Save")
        self.cancelButton = QPushButton("Close")
        self.defaultButton = QPushButton("Restore Defaults")

        self.okButton.clicked.connect(self.saveSettings)
        self.cancelButton.clicked.connect(self.parentWidget().close)
        self.defaultButton.clicked.connect(self.restoreDefaults)

        buttonBar.layout().addWidget(self.defaultButton)
        buttonBar.layout().addStretch()
        buttonBar.layout().addWidget(self.okButton)
        buttonBar.layout().addWidget(self.cancelButton)

        self.layout().addWidget(buttonBar, row, 0, 1, -1, alignment=Qt.AlignBottom)

    def updateUI(self):
        self.loadSettings()

    def saveSettings(self):
        pass

    def restoreDefaults(self):
        try:
            remove(self.settings.fileName())
        except FileNotFoundError:
            pass
        self.updateUI()


class ViewSettings(SettingsTab):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

        self.setLayout(QGridLayout(self))
        self.loadSettings()
        self.initButtons()
        self.initLiveView()
        self.updateLiveView()
        self.addButtonBar(self.layout().rowCount())

# ----------------------------------- View Updates ----------------------------------- #

    # It would make more sense if this is a PreviewContainer method. However,
    # this requires the configuration-related methods to be moved as well.
    def stylePreviewText(self, font, padding, color, background):
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

    def updateLiveView(self, inSettings = True):

        def colorToRGBA(objectName):
            # Convert QColor to a QSS string of the following format:
            # "rgba(<red>, <green>, <blue>, <alpha>)"
            _c = getattr(self, objectName)
            if self._properties[objectName] == 'rgba':
                color = f"rgba({_c.red()}, {_c.green()}, {_c.blue()}, {_c.alpha()})"
                return color

        # Update preview text style
        styles = self.stylePreviewText(self.previewFont, self.previewPadding,
            colorToRGBA('previewColor'), colorToRGBA('previewBackground'))
        
        # Update window background color
        # TODO: Window color is not set properly since parent color is different
        # BUG: Styles are not being applied to liveView object
        _windowColor = colorToRGBA('windowColor')
        
        # Set stylesheet and update selection rubberband
        if inSettings:
            self.setStyleSheet(styles)
            self._liveView.rubberBand.setFill(self.selectionBackground)
            self._liveView.rubberBand.setBorder(self.selectionBorderColor, 
                self.selectionBorderThickness)
        elif not inSettings:
            self.parent.setStyleSheet(styles)
            self._rubberBand.setFill(self.selectionBackground)
            self._rubberBand.setBorder(self.selectionBorderColor, 
                self.selectionBorderThickness)

    def updateUI(self):
        self.loadSettings()
        self.updateLiveView()

# ------------------------------------- Settings ------------------------------------- #

    def saveSettings(self):
        for propName, _ in self._properties.items():
            self.settings.setValue(propName, getattr(self, propName))

    def loadSettings(self):
        self.settings = QSettings("./utils/Manga2OCR-view.ini", QSettings.IniFormat)
        # Properties and defaults
        self._defaults = {
            # Preview
            'previewFont': QFont("Arial", 16),
            'previewColor': QColor(239, 240, 241, 255),
            'previewBackground': QColor(72, 75, 106, 230),
            'previewPadding': 10,
            # Selection rubberband
            'selectionBorderColor': QColor(0, 128, 255, 255),
            'selectionBorderThickness': 2,
            'selectionBackground': QColor(0, 128, 255, 60),
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
                # Find the property in settings
                # Set it as the value if it exists
                if propType == 'rgba':
                    prop = self.settings.value(propName)
                elif propType == 'color':
                    prop = self.settings.value(propName)
                elif propType == 'dist':
                    prop = int(self.settings.value(propName))
                elif propType == 'font':
                    prop = self.settings.value(propName)
                if self.settings.contains(propName):
                    setattr(self, propName, prop)
                else: raise TypeError
            except:
                # Property does not exist in settings
                # Use default value
                setattr(self, propName, self._defaults[propName])

# -------------------------------- UI Initializations -------------------------------- #

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
        self._liveView = PreviewContainer(self)
        self._rubberBand = self.findChild(QRubberBand, "selectionBand")
        self.layout().addWidget(self._liveView, 2, 0, 1, -1)
        self.layout().setRowStretch(self.layout().rowCount()-1, 1)

# --------------------------- Property Setters and Getters --------------------------- #

    def setProperty_(self, objectName, value):
        # Set the value of a member of this class with name objectName
        setattr(self, objectName, value)
        self.updateLiveView()

    def getColor_(self, objectName):
        try:
            initialColor = getattr(self, objectName)
        except:
            initialColor = None
        if initialColor is None:
            initialColor = self._defaults[objectName]
        color = QColorDialog().getColor(initial=initialColor, options=QColorDialog.ShowAlphaChannel)
        if color.isValid():
            self.setProperty_(objectName, color)

    def getFont_(self, objectName):
        try:
            initialFont = getattr(self, objectName)
        except:
            initialFont = None
        if initialFont is None:
            initialFont = self._defaults[objectName]
        font, accepted = QFontDialog().getFont(initialFont)
        if accepted:
            self.setProperty_(objectName, font)

    def getInt_(self, objectName):
        try:
            initialInt = int(getattr(self, objectName))
        except:
            initialInt = None
        if initialInt is None:
            initialInt = self._defaults[objectName]
        i, accepted = QInputDialog.getInt(
            self,
            "Margin/Padding Settings",
            "Enter a value between 1 and 50:",
            value=initialInt,
            min=1,
            max=50,
            flags=Qt.CustomizeWindowHint | Qt.WindowTitleHint)

        if accepted:
            self.setProperty_(objectName, i)

class HotkeySettings(SettingsTab):

    class HotkeyContainer(QWidget):

        def __init__(self, shortcutName):
            super().__init__()

            # Layout and margins
            self.setLayout(QHBoxLayout(self))
            self.layout().setAlignment(Qt.AlignTop)
            _margin = self.layout().contentsMargins()
            _margin.setBottom(0)
            _margin.setTop(7)
            self.layout().setContentsMargins(_margin)

            self.initButtons(shortcutName)
            self.loadSettings()

        # ---------------------------- UI Initializations ---------------------------- #

        def initButtons(self, shortcutName):
            self.shortcutName = QLabel(shortcutName)

            # Modifiers
            self.shiftCheckBox = QCheckBox("Shift")
            self.ctrlCheckBox = QCheckBox("Ctrl")
            self.altCheckBox = QCheckBox("Alt")
            # self.winCheckBox = QCheckBox("Win")

            # Key
            _validKeyList = ["<Unmapped>", "A", "B", "C", "D", "E", "F", "G", 
                            "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q",
                            "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
            self.keyComboBox = QComboBox()
            self.keyComboBox.addItems(_validKeyList)

            # Layout
            self.layout().addWidget(self.shortcutName, alignment=Qt.AlignLeft)
            self.layout().addStretch()
            self.layout().addWidget(self.shiftCheckBox, alignment=Qt.AlignRight)
            self.layout().addWidget(self.ctrlCheckBox, alignment=Qt.AlignRight)
            self.layout().addWidget(self.altCheckBox, alignment=Qt.AlignRight)
            # self.layout().addWidget(self.winCheckBox, alignment=Qt.AlignRight)
            self.layout().addWidget(self.keyComboBox, alignment=Qt.AlignRight)

        # --------------------------------- Settings --------------------------------- #

        def saveSettings(self):
            _shortcut = ""
            _shortcut += "Shift+" * self.shiftCheckBox.isChecked()
            _shortcut += "Ctrl+" * self.ctrlCheckBox.isChecked()
            _shortcut += "Alt+" * self.altCheckBox.isChecked()
            # _shortcut += "Win+" * self.winCheckBox.isChecked()

            _key = self.keyComboBox.currentText()
            if _key == "<Unmapped>": _key = ""
            _shortcut += _key

            for propName, propObject in self._properties.items():
                try:
                    prop = getattr(self, propObject).isChecked()
                except AttributeError:
                    prop = getattr(self, propObject).currentIndex()
                self.settings.setValue(propName, int(prop))

            _shortcutText = self.shortcutName.text().split(" ")
            _shortcutName = _shortcutText[0].lower() + "".join(s.title() for s in _shortcutText[1:])

            return _shortcut, _shortcutName

        def loadSettings(self):
            self.settings = QSettings("./utils/Manga2OCR-hotkey.ini", QSettings.IniFormat)

            # Properties and defaults
            _shortcutText = self.shortcutName.text().split(" ")
            _shortcutName = _shortcutText[0].lower() + "".join(s.title() for s in _shortcutText[1:])
            self._properties = {
                f"{_shortcutName}Shift": 'shiftCheckBox',
                f"{_shortcutName}Ctrl": 'ctrlCheckBox',
                f"{_shortcutName}Alt": 'altCheckBox',
                # f"{_shortcutName}Cmd": 'winCheckBox',
                f"{_shortcutName}Key": 'keyComboBox'
            }
            self._defaults = {
                "startCaptureAlt": True,
                "startCaptureKey": 17 # index of Q in _validKeyList
            }

            def setObjectState(objectName, objectState):
                # Check if the object is a checkbox or combo box
                try:
                    getattr(self, objectName).setChecked(objectState)
                except AttributeError:
                    getattr(self, objectName).setCurrentIndex(objectState)

            for propName, propObject in self._properties.items():
                try:
                    # Override default state if saved in settings
                    if self.settings.contains(propName):
                        prop = self.settings.value(propName, type=int)
                        setObjectState(propObject, prop)
                    else: raise TypeError
                except:
                    # Set default state if it exists
                    if propName in self._defaults:
                        setObjectState(propObject, self._defaults[propName])
                        continue
                    # No existing default or saved settings
                    # Therefore, action is unmapped
                    setObjectState(propObject, 0)

# -------------------------------- UI Initializations -------------------------------- #

    def __init__(self, parent):
        super().__init__(parent)
        self.settings = QSettings("./utils/Manga2OCR-hotkey.ini", QSettings.IniFormat)

        # Layout and margins
        self.setLayout(QGridLayout(self))
        self.layout().setAlignment(Qt.AlignTop)

        self.addHotkeyContainers()
        self.layout().addWidget(QWidget())
        self.layout().setRowStretch(self.layout().rowCount()-1, 1)
        self.addButtonBar(self.layout().rowCount())

    def addHotkeyContainers(self):
        self.containerList = []
        _actionList = ["Start Capture",
                       "Toggle Logging",
                       "Open Settings",
                       "Close Application"]
        for _action in _actionList:
            self.containerList.append(self.HotkeyContainer(_action))
            self.layout().addWidget(self.containerList[-1])

# ------------------------------------- Settings ------------------------------------- #

    def saveSettings(self):
        _h = {}
        for container in self.containerList:
            hotkey, action = container.saveSettings()
            _h[action] = hotkey
        self.settings.setValue('hotkeys', _h)
    
    def loadSettings(self):
        for container in self.containerList:
            container.loadSettings()

class SettingsMenu(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.tabs = QTabWidget()
        self.tabs.addTab(HotkeySettings(self), "HOTKEYS")
        self.tabs.addTab(ViewSettings(self), "VIEW")

        self.setLayout(QVBoxLayout(self))
        self.layout().addWidget(self.tabs)
        self.setFixedSize(625, 400)

