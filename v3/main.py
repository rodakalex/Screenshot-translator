import asyncio
import time

import pyrogram
import sys

from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPainter, QBrush, QColor
from PyQt5.QtWidgets import *

import config


class ScreenshotWindow(QMainWindow):
    def __init__(self, main_app: QMainWindow):
        super().__init__()
        self.setWindowTitle("Screenshot Tool")
        self.app = main_app
        self.setGeometry(100, 100, 800, 600)
        self.label = QLabel(self)
        self.label.setGeometry(0, 0, 800, 600)
        self.setWindowOpacity(0)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setMouseTracking(True)
        self.drawing = False
        self.start_x, self.start_y = 0, 0
        self.end_x, self.end_y = 0, 0

    def closeEvent(self, event):
        self.app.quit()

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


class QLabelBuddy(QDialog):
    def __init__(self):
        super().__init__()
        self.layout = None
        self.init_ui()
        self.app = pyrogram.Client(config.name, config.api_id, config.api_hash)
        self.message_text = None

    def translate_text(self):
        self.app.run(self.async_translate_text(self.text_to_translate.toPlainText()))
        self.text_translate.setPlainText(self.message_text)

    async def async_translate_text(self, text):
        try:
            await self.app.start()
            await self.app.send_message(chat_id='YTranslateBot', text=text)
            await asyncio.sleep(1)
            async for message in self.app.get_chat_history(chat_id='YTranslateBot', limit=1, offset_id=-1):
                self.message_text = message.text

        except Exception as e:
            print(e)

        finally:
            await self.app.stop()

    def handle_translation(self, result):
        self.message_text = result

    def init_ui(self):
        self.layout = QVBoxLayout(self)
        self.setWindowTitle("Qua!")

        title_to_translate = QLabel('&Текст', self)
        title_to_translate.setAlignment(Qt.AlignTop)
        title_to_translate.setWordWrap(True)
        self.text_to_translate = QPlainTextEdit(self)
        self.text_to_translate.setFixedHeight(100)
        title_to_translate.setBuddy(self.text_to_translate)

        self.layout.addWidget(title_to_translate)
        self.layout.addWidget(self.text_to_translate)

        title_translate = QLabel('&Перевод', self)
        title_translate.setAlignment(Qt.AlignTop)
        title_translate.setWordWrap(True)
        self.text_translate = QPlainTextEdit(self)
        self.text_translate.setReadOnly(True)
        self.text_translate.setFixedHeight(100)
        title_translate.setBuddy(self.text_translate)

        translate_btn = QPushButton("&Перевести", self)
        translate_btn.setFixedSize(100, 30)
        translate_btn.clicked.connect(self.translate_text)

        screen_btn = QPushButton("&Скриншот", self)
        screen_btn.setFixedSize(100, 30)
        screen_btn.clicked.connect(make_screen)  # На эту кнопку должна вызываться подпрограмма

        self.layout.addWidget(title_translate)
        self.layout.addWidget(self.text_translate)
        self.layout.addWidget(translate_btn)
        self.layout.addWidget(screen_btn)


def make_screen():
    screen_window.setWindowOpacity(0.1)


if __name__ == '__main__':
    app = QApplication([])
    main = QLabelBuddy()
    screen_window = ScreenshotWindow(app)
    screen_window.showFullScreen()

    main.show()
    screen_window.showFullScreen()
    sys.exit(main.exec_())
