import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QFrame
from PyQt5.QtGui import QPainter, QColor, QBrush
from PyQt5.QtCore import Qt, QRect


class ScreenshotWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Screenshot Tool")
        self.setGeometry(100, 100, 800, 600)
        self.label = QLabel(self)
        self.label.setGeometry(0, 0, 800, 600)
        self.setWindowOpacity(0.1)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setMouseTracking(True)
        self.drawing = False
        self.start_x, self.start_y = 0, 0
        self.end_x, self.end_y = 0, 0

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.start_x, self.start_y = event.x(), event.y()

    def mouseMoveEvent(self, event):
        if self.drawing:
            self.end_x, self.end_y = event.x(), event.y()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.drawing:
            self.drawing = False
            screenshot_rect = QRect(min(self.start_x, self.end_x), min(self.start_y, self.end_y),
                                    abs(self.end_x - self.start_x), abs(self.end_y - self.start_y))
            self.setWindowOpacity(0)

            screenshot = QApplication.primaryScreen().grabWindow(0, screenshot_rect.x(), screenshot_rect.y(),
                                                                 screenshot_rect.width(), screenshot_rect.height())
            screenshot.save("screenshot.png", "PNG")
            self.close()

    def paintEvent(self, event):
        if self.drawing:
            painter = QPainter(self)
            overlay_color = QColor(255, 255, 255, 100)
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(overlay_color))
            painter.drawRect(QRect(0, 0, self.width(), self.height()))
            painter.setBrush(Qt.NoBrush)
            painter.setPen(Qt.SolidLine)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setPen(QColor(0, 0, 0))
            painter.drawRect(QRect(self.start_x, self.start_y, self.end_x - self.start_x, self.end_y - self.start_y))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ScreenshotWindow()
    window.showFullScreen()
    sys.exit(app.exec_())
