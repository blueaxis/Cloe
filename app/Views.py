"""
Poricom View Components

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

from PyQt5.QtGui import (QPixmap, QPalette, QBrush, QColor, QFont)
from PyQt5.QtCore import (Qt, QTimer, QThreadPool, pyqtSlot, QPoint, QSettings)
from PyQt5.QtCore import (Qt, QRect, QSize, QTimer, QThreadPool, pyqtSlot)
from PyQt5.QtWidgets import (QMainWindow,
    QRubberBand, QGraphicsOpacityEffect, QApplication, QGraphicsView, QLabel)

from Workers import BaseWorker
from Settings import ViewSettings, CustomBand
from utils.image_io import logText, pixboxToText

class BaseCanvas(QGraphicsView):

    def __init__(self, parent=None, tracker=None):
        super(QGraphicsView, self).__init__(parent)
        self.parent = parent
        self.tracker = tracker

        self._timer = QTimer()
        self._timer.setInterval(300)
        self._timer.setSingleShot(True)
        self._timer.timeout.connect(self.rubberBandStopped)

        self._initialPoint = QPoint()
        self._rubberBand = CustomBand(CustomBand.Rectangle, self.parent)

        self._canvasText = QLabel("", self.parent, Qt.WindowStaysOnTopHint)
        self._canvasText.setWordWrap(True)
        self._canvasText.hide()
        self._canvasText.setObjectName("canvasText")

        self.pixmap = QPixmap()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._initialPoint = event.pos()
            self._rubberBand.setGeometry(QRect(self._initialPoint, QSize()))
            self._rubberBand.show()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if ((event.buttons() & Qt.LeftButton)):
            self._timer.start()
            self._rubberBand.setGeometry(
                QRect(self._initialPoint, event.pos()).normalized())
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if (event.button() == Qt.LeftButton):
            self._rubberBand.setGeometry(
                QRect(self._initialPoint, event.pos()).normalized())

            logPath = self.tracker.filepath + "/log.txt"
            logToFile = self.tracker.writeMode
            text = self._canvasText.text()
            logText(text, mode=logToFile, path=logPath)
            self._rubberBand.hide()
            self._canvasText.hide()

        super().mouseReleaseEvent(event)

    @pyqtSlot()
    def rubberBandStopped(self):

        if (self._canvasText.isHidden()):
            self._canvasText.setText("")
            self._canvasText.adjustSize()
            self._canvasText.show()

        lang = self.tracker.language + self.tracker.orientation

        screen = QApplication.primaryScreen()
        s = screen.size()
        self.pixmap = screen.grabWindow(0).scaled(s.width(), s.height())
        pixbox = self.pixmap.copy(self._rubberBand.geometry())

        _worker = BaseWorker(pixboxToText, pixbox, lang, self.tracker.ocrModel)
        _worker.signals.result.connect(self._canvasText.setText)
        _worker.signals.finished.connect(self._canvasText.adjustSize)
        self._timer.timeout.disconnect(self.rubberBandStopped)
        _worker.signals.finished.connect(
            lambda: self._timer.timeout.connect(self.rubberBandStopped))
        QThreadPool.globalInstance().start(_worker)


class FullScreen(BaseCanvas):

    def __init__(self, parent=None, tracker=None):
        super().__init__(parent, tracker)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setGraphicsEffect(QGraphicsOpacityEffect(opacity=0.05))
        self.restoreSettings()
        self.updateLiveView()

    # TODO: Try to inherit these from ViewSettings
    # The mouse click event doesn't work when inheriting from ViewSettings
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
            QLabel#canvasText {{ 
                color: {_previewColor};
                background-color: {_previewBackground}; 
                padding: {_previewPadding};
                font-family: {self.previewFont.family()};
                font-size: {self.previewFont.pointSize()}pt;
                margin-top: 0.02em;
                margin-left: 0.02em;
            }}
        """
        self.parent.setStyleSheet(styles)

        # BUG: Rubberband not updating on start
        palette = QPalette()
        palette.setBrush(QPalette.Highlight, QBrush(self.selectionBackground))
        self._rubberBand.setPalette(palette)
        self._rubberBand.setBorder(self.selectionBorderColor, self.selectionBorderThickness)

    def mouseReleaseEvent(self, event):
        BaseCanvas.mouseReleaseEvent(self, event)
        self.parent.close()


class ExternalWindow(QMainWindow):
    def __init__(self, tracker):
        super().__init__()
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet("border:0px; margin:0px")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        self.setCentralWidget(FullScreen(self, tracker))
