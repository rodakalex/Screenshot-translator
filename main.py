import asyncio

import pyrogram
import sys

import pytesseract
from PIL import Image
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPainter, QBrush, QColor
from PyQt5.QtWidgets import *
from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models.gigachat import GigaChat

import config

pytesseract_string = None


class ScreenshotWindow(QMainWindow):
    def __init__(self, main_app):
        super().__init__()
        self.pytesseract_string = None
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
            image = Image.open('screenshot.png')
            res_text_screen = pytesseract.image_to_string(image, lang='eng').lower().replace("\n", " ")
            self.app.text_to_translate.setPlainText(res_text_screen)
            self.app.translate_text()

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
        self.text_translate = None
        self.text_to_translate = None
        self.layout = None
        self.init_ui()
        self.app = pyrogram.Client(config.name, config.api_id, config.api_hash)
        self.message_text = None

    def translate_giga_chat_bot(self, text):
        # TODO:
        #  1. Добавить эти инициализации в класс если задан определённый параметр
        messages = [
            SystemMessage(
                content="Переведи текст"
            )
        ]

        chat = GigaChat(
            credentials=config.credentials,
            verify_ssl_certs=False)

        messages.append(HumanMessage(content=f'Переведи: {text}'))
        res = chat(messages)
        messages.append(res)

        self.message_text = res.content

    def translate_text(self):
        if config.SETTINGS['choose_translate'] == 'gigachat':
            self.translate_giga_chat_bot(self.text_to_translate.toPlainText())

        else:
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

    def init_ui(self):
        self.layout = QVBoxLayout(self)
        self.setWindowTitle("Qua!")

        title_to_translate = QLabel('&Текст', self)
        title_to_translate.setAlignment(Qt.AlignTop)
        title_to_translate.setWordWrap(True)
        self.text_to_translate = QPlainTextEdit(self)
        self.text_to_translate.setFixedHeight(150)
        self.text_to_translate.setFixedWidth(500)
        title_to_translate.setBuddy(self.text_to_translate)

        self.layout.addWidget(title_to_translate)
        self.layout.addWidget(self.text_to_translate)

        title_translate = QLabel('&Перевод', self)
        title_translate.setAlignment(Qt.AlignTop)
        title_translate.setWordWrap(True)
        self.text_translate = QPlainTextEdit(self)
        self.text_translate.setReadOnly(True)
        self.text_translate.setFixedHeight(150)
        self.text_to_translate.setFixedWidth(500)
        self.text_translate.setPlainText(pytesseract_string)

        title_translate.setBuddy(self.text_translate)

        translate_btn = QPushButton("&Перевести", self)
        translate_btn.setFixedSize(100, 30)
        translate_btn.clicked.connect(self.translate_text)

        screen_btn = QPushButton("&Скриншот", self)
        screen_btn.setFixedSize(100, 30)
        screen_btn.clicked.connect(lambda make_screen: screen_window.setWindowOpacity(0.1))

        self.layout.addWidget(title_translate)
        self.layout.addWidget(self.text_translate)
        self.layout.addWidget(translate_btn)
        self.layout.addWidget(screen_btn)


if __name__ == '__main__':
    # TODO:
    #  1. Убрать мёртвый код +
    #  2. Добавить переводчик от deepl
    #  3. Задать горячие клавиши
    #  4. Исправить проблему с окнами

    q_application = QApplication([])
    q_label_buddy = QLabelBuddy()
    screen_window = ScreenshotWindow(q_label_buddy)
    screen_window.showFullScreen()

    q_label_buddy.show()
    screen_window.show()
    sys.exit(q_label_buddy.exec_())
