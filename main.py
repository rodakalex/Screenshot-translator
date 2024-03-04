import json
import sys

import requests
from PIL import Image
from PyQt5.QtCore import Qt, QRect, QEventLoop
from PyQt5.QtGui import QPainter, QBrush, QColor
from PyQt5.QtWidgets import *
from pytesseract import pytesseract

from IMMUTABLE_WORDS import immutable_words

pytesseract_string = None


def make_first_letter_is_upper(sentence: str):
    try:
        return f'{sentence[0].upper()}{sentence[1:]}'
    except IndexError:
        return ''


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

            screenshot = QApplication.primaryScreen().grabWindow(0, screenshot_rect.x(), screenshot_rect.y(),
                                                                 screenshot_rect.width(), screenshot_rect.height())
            # Можно закомментировать для отладки
            screenshot.save("screenshot.png", "PNG")
            image = Image.open('screenshot.png')

            text_from_screen: str = pytesseract.image_to_string(image, lang='eng')
            metamorph_text = text_from_screen.lower().replace("\n", " ")

            for immutable_word in immutable_words:
                metamorph_text = metamorph_text.replace(immutable_word, immutable_words.get(immutable_word))

            metamorph_text = '. '.join(map(make_first_letter_is_upper, metamorph_text.split('. ')))

            after_metamorph = metamorph_text
            print(after_metamorph)

            self.app.text_to_translate.setPlainText(after_metamorph)
            self.app.translate_text()
            self.close()

    def paintEvent(self, a0, event=None):
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
        self.message_text = None

    def translate_text(self):
        self.libretranslate_translate_text(self.text_to_translate.toPlainText())
        self.text_translate.setPlainText(self.message_text)

    def libretranslate_translate_text(self, text):
        url = "http://127.0.0.1:5000/translate"
        data = {
            "q": f"{text}",
            "source": "en",
            "target": "ru",
            "format": "text",
            "api_key": ""
        }
        headers = {"Content-Type": "application/json"}
        post = requests.post(url, data=json.dumps(data), headers=headers)

        if post.status_code == 200:
            self.message_text = post.json()['translatedText']

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
        screen_btn.clicked.connect(create_screenshot_window)

        self.layout.addWidget(title_translate)
        self.layout.addWidget(self.text_translate)
        self.layout.addWidget(translate_btn)
        self.layout.addWidget(screen_btn)


def create_screenshot_window():
    screen_window = ScreenshotWindow(q_label_buddy)
    screen_window.show()
    screen_window.setWindowOpacity(0.1)
    screen_window.showFullScreen()
    # Если нужно отдебажить захват с экрана
    # screen_window.show()
    event_loop = QEventLoop()
    event_loop.exec_()


if __name__ == '__main__':
    # TODO:
    #  1. Задать горячие клавиши
    #  2. Написать файл инсталлера
    #  3. Добавить всегда большую букву после точки
    #  4. Добавить обработку спецсимволов
    #  5. Написать интерфейс для автоисправления
    #  6. Написать окно настроек программы
    #  7. Подключить SpellChecker

    q_application = QApplication([])
    q_label_buddy = QLabelBuddy()
    q_label_buddy.show()

    sys.exit(q_label_buddy.exec_())
