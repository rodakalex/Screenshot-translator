import asyncio
import pyrogram
import sys

from PyQt5.QtCore import Qt, QRect, QObject, pyqtSignal, QRunnable, pyqtSlot
from PyQt5.QtWidgets import *

import take_screen

import config


class WorkerSignals(QObject):
    result = pyqtSignal(object)


class AsyncWorker(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super().__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        result = self.fn(*self.args, **self.kwargs)
        self.signals.result.emit(result)


class QLabelBuddy(QDialog):
    def __init__(self):
        super().__init__()
        self.layout = None
        self.init_ui()
        # self.init_async_ui()
        self.app = pyrogram.Client(config.name, config.api_id, config.api_hash)
        self.message_text = None

    def translate_text(self):
        self.app.run(self.acync_translate_text(self.text_to_translate.toPlainText()))
        self.text_translate.setPlainText(self.message_text)

    async def acync_translate_text(self, text):
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

        self.layout.addWidget(title_translate)
        self.layout.addWidget(self.text_translate)
        self.layout.addWidget(translate_btn)

    # async def init_async_ui(self):
    #     translate_btn = QPushButton("&Перевести", self)
    #     translate_btn.clicked.connect(await self.acync_translate_text)
    #     translate_btn.setFixedSize(100, 30)
    #
    #     self.layout.addWidget(translate_btn)


if __name__ == '__main__':
    app = QApplication([])
    main = QLabelBuddy()
    main.show()
    sys.exit(app.exec_())
