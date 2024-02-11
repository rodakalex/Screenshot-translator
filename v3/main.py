import asyncio
import pyrogram
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPainter, QColor, QBrush
from PyQt5.QtWidgets import *
import sys

import config


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


class Translation:
    def __init__(self):
        self.app = pyrogram.Client(config.name, config.api_id, config.api_hash)
        self.message_text = None

    async def translate_text(self, text):
        try:
            await self.app.start()
            await self.app.send_message(chat_id='YTranslateBot', text=text)
            await asyncio.sleep(1)
            async for message in self.app.get_chat_history(chat_id='YTranslateBot', limit=1, offset_id=-1):
                self.message_text = message.text

            await self.app.stop()
        except Exception as e:
            print(e)


class QLabelBuddy(QDialog):
    def __init__(self):
        super().__init__()
        self.translation = Translation()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        self.setWindowTitle("Qua!")

        title_to_translate = QLabel('&Текст', self)
        title_to_translate.setAlignment(Qt.AlignTop)
        title_to_translate.setWordWrap(True)
        text_to_translate = QPlainTextEdit(self)
        text_to_translate.setFixedHeight(100)
        title_to_translate.setBuddy(text_to_translate)

        layout.addWidget(title_to_translate)
        layout.addWidget(text_to_translate)

        title_translate = QLabel('&Перевод', self)
        title_translate.setAlignment(Qt.AlignTop)
        title_translate.setWordWrap(True)
        text_translate = QPlainTextEdit(self)
        text_translate.setReadOnly(True)
        text_translate.setFixedHeight(100)
        title_translate.setBuddy(text_translate)

        translate_btn = QPushButton("&Перевести", self)
        translate_btn.setFixedSize(100, 30)

        layout.addWidget(title_translate)
        layout.addWidget(text_translate)
        layout.addWidget(translate_btn)


if __name__ == '__main__':
    app = QApplication([])
    main = QLabelBuddy()
    main.show()
    sys.exit(app.exec_())
