from PyQt5.QtGui import (QColor, QPainter, QPen)
from PyQt5.QtCore import (Qt)
from PyQt5.QtWidgets import (QLabel, QRubberBand, QGridLayout, QWidget)


class CustomBand(QRubberBand):

    def __init__(self, shape, parent,
                 borderColor=Qt.blue, thickness=2, fillColor=QColor(0, 128, 255, 60)):
        super().__init__(shape, parent)
        self.setBorder(borderColor, thickness)
        self.setFill(fillColor)

    def setBorder(self, color, thickness):
        self._borderColor = color
        self._borderThickness = thickness

    def setFill(self, color):
        self._fillColor = color

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        # Mask
        painter.fillRect(event.rect(), self._fillColor)
        # Border
        painter.setPen(QPen(self._borderColor, self._borderThickness))
        painter.drawRect(event.rect())
        painter.end()
        # return super().paintEvent(event)


class PreviewContainer(QWidget):

    def __init__(self, parent):
        super().__init__(parent)
        self.setObjectName("liveView")
        self.setLayout(QGridLayout(self))

        self.createPreviewText()
        self.createSelectionBand()

# ----------------------------------- View Updates ----------------------------------- #

    def resizeEvent(self, event):
        if self is not None:
            # Resize rubber band when window size is changed
            w = 0.4 * self.width()
            y = 0.05 * self.height()
            x = self.width() - w - y
            h = self.height() - 2*y
            self.rubberBand.setGeometry(x, y, w, h)
        return super().resizeEvent(event)

# -------------------------------- UI Initializations -------------------------------- #

    def createSelectionBand(self):
        self.rubberBand = CustomBand(CustomBand.Rectangle, self)
        self.rubberBand.setObjectName("selectionBand")
        self.rubberBand.show()

    def createPreviewText(self, text=" Sample Text"):
        self._previewText = QLabel(text)
        self._previewText.setObjectName("previewText")
        self._previewText.adjustSize()
        self.layout().addWidget(self._previewText, 0, 0,
                                alignment=Qt.AlignTop | Qt.AlignLeft)

    def setBackgroundColor(self, color):
        self.backgroundColor = color

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)

        # Draw alpha background
        # Adopted from: https://sourceforge.net/projects/capture2text/
        squareSize = 20
        numSquaresX = int(self.width() / squareSize) + 1
        numSquaresY = int(self.height() / squareSize) + 1
        for y in range(numSquaresY):
            isWhite = ((y % 2) == 0)
            for x in range(numSquaresX):
                color = QColor(200, 200, 200, 255)
                if(isWhite):
                    color.setRgb(255, 255, 255, 255)
                painter.fillRect(x * squareSize, y * squareSize,
                                 squareSize, squareSize, color)
                isWhite = not isWhite
        # Draw true background
        painter.fillRect(0, 0, self.width(), self.height(),
                         self.backgroundColor)
        # Draw border
        painter.setPen(QPen(QColor(0, 0, 0), 2))
        painter.drawRect(0, 0, self.width(), self.height())

        painter.end()
        return super().paintEvent(event)
