"""
Cloe OCR View Components

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

from PyQt5.QtCore import Qt, QThreadPool, QTimer, QPoint, QRect, QSize, pyqtSlot
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QGraphicsView, QLabel, QWidget

from components.misc import RubberBand
from components.services import BaseWorker
from utils.scripts import logText, pixmapToText


class BaseOCRView(QGraphicsView):
    """
    Base view with OCR capabilities
    """

    def __init__(self, parent: QWidget):
        super().__init__(parent)

        self._timer = QTimer()
        self._timer.setInterval(300)
        self._timer.setSingleShot(True)
        self._timer.timeout.connect(self.rubberBandStopped)

        self._initialPoint = QPoint()
        self.rubberBand = RubberBand(self.parent())

        self._ocrText = QLabel("", self.parent(), Qt.WindowStaysOnTopHint)
        self._ocrText.setWordWrap(True)
        self._ocrText.hide()
        self._ocrText.setObjectName("previewText")

        self.pixmap = QPixmap()

    # -------------------------------------- Mouse -------------------------------------- #

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._initialPoint = event.pos()
            self.rubberBand.setGeometry(QRect(self._initialPoint, QSize()))
            self.rubberBand.show()
        return super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self._timer.start()
            self.rubberBand.setGeometry(
                QRect(self._initialPoint, event.pos()).normalized()
            )
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.rubberBand.setGeometry(
                QRect(self._initialPoint, event.pos()).normalized()
            )

            text = self._ocrText.text()
            logText(text)
            self.rubberBand.hide()
            self._ocrText.hide()

        super().mouseReleaseEvent(event)

    @pyqtSlot()
    def rubberBandStopped(self):

        if self._ocrText.isHidden():
            self._ocrText.setText("")
            self._ocrText.adjustSize()
            self._ocrText.show()

        screen = QApplication.primaryScreen()
        s = screen.size()
        self.pixmap = screen.grabWindow(0).scaled(s.width(), s.height())
        pixmap = self.pixmap.copy(self.rubberBand.geometry())

        worker = BaseWorker(pixmapToText, pixmap, self.parent().ocrModel)
        worker.signals.result.connect(self.ocrFinished)
        self._timer.timeout.disconnect(self.rubberBandStopped)
        QThreadPool.globalInstance().start(worker)

    # -------------------------------------- Close -------------------------------------- #

    def closeEvent(self, event):
        # Ensure that object is deleted before closing
        self.deleteLater()
        return super().closeEvent(event)

    def ocrFinished(self, text):
        try:
            self._ocrText.setText(text)
            self._ocrText.adjustSize()
            self._timer.timeout.connect(self.rubberBandStopped)
        except Exception as e:
            print(e)
