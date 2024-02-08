import pytesseract
from PIL import Image


def get_text_from_screen() -> str:
    image = Image.open('../../screenshot.png')
    return pytesseract.image_to_string(image, lang='eng')


def get_formatter_text():
    return get_text_from_screen().lower().replace("\n", " ")
