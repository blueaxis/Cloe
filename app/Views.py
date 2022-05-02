"""
Cloe Fullscreen View Component

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

from PyQt5.QtGui import (QPixmap, QCursor)
from PyQt5.QtCore import (Qt, QThreadPool, QTimer,
                          QPoint, QRect, QSize, pyqtSlot)
from PyQt5.QtWidgets import (QApplication, QMainWindow, QGraphicsView, QLabel)

from Workers import BaseWorker
from Settings import ViewSettings
from Preview import CustomBand
from utils.image_io import logText, pixboxToText


class BaseCanvas(QGraphicsView):

    def __init__(self, parent=None):
        QGraphicsView.__init__(self, parent)
        self.parent = parent

        self._timer = QTimer()
        self._timer.setInterval(300)
        self._timer.setSingleShot(True)
        self._timer.timeout.connect(self.rubberBandStopped)

        self._initialPoint = QPoint()
        self._rubberBand = CustomBand(CustomBand.Rectangle, self.parent)

        self._canvasText = QLabel("", self.parent, Qt.WindowStaysOnTopHint)
        self._canvasText.setWordWrap(True)
        self._canvasText.hide()
        self._canvasText.setObjectName("previewText")

        self.pixmap = QPixmap()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._initialPoint = event.pos()
            self._rubberBand.setGeometry(QRect(self._initialPoint, QSize()))
            self._rubberBand.show()
        return super().mousePressEvent(event)

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

            # TODO: Track log path and log mode in QSettings instead
            text = self._canvasText.text()
            logText(text)
            self._rubberBand.hide()
            self._canvasText.hide()

        super().mouseReleaseEvent(event)

    @pyqtSlot()
    def rubberBandStopped(self):

        if (self._canvasText.isHidden()):
            self._canvasText.setText("")
            self._canvasText.adjustSize()
            self._canvasText.show()

        screen = QApplication.primaryScreen()
        s = screen.size()
        self.pixmap = screen.grabWindow(0).scaled(s.width(), s.height())
        pixbox = self.pixmap.copy(self._rubberBand.geometry())

        _worker = BaseWorker(pixboxToText, pixbox, self.parent.ocrModel)
        _worker.signals.result.connect(self.ocrFinished)
        self._timer.timeout.disconnect(self.rubberBandStopped)
        QThreadPool.globalInstance().start(_worker)

    def closeEvent(self, event):
        # Ensure that object is deleted before closing
        self.deleteLater()
        return super().closeEvent(event)

    def ocrFinished(self, text):
        try:
            self._canvasText.setText(text)
            self._canvasText.adjustSize()
            self._timer.timeout.connect(self.rubberBandStopped)
        except Exception as e:
            print(e)


class FullScreen(BaseCanvas, ViewSettings):

    def __init__(self, parent=None):
        BaseCanvas.__init__(self, parent)

        # View Initializations
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Restore settings and update view
        self._liveView = None
        self.loadSettings()
        self.updateLiveView(inSettings=False)

    def setBackgroundColor(self, color):
        self.setStyleSheet(f"background-color: {color}")

    def mouseReleaseEvent(self, event):
        BaseCanvas.mouseReleaseEvent(self, event)
        self.parent.close()


class ExternalWindow(QMainWindow):
    def __init__(self, parent):
        super().__init__()
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet("border:0px; margin:0px")
        self.setWindowFlags(Qt.FramelessWindowHint |
                            Qt.WindowStaysOnTopHint | Qt.Popup)
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        QApplication.setOverrideCursor(QCursor(Qt.CrossCursor))

        self.setCentralWidget(FullScreen(self))

        self.ocrModel = parent.ocrModel

    def closeEvent(self, event):
        # Ensure that object is deleted before closing
        self.deleteLater()
        # Restore cursor
        QApplication.restoreOverrideCursor()
        return super().closeEvent(event)
