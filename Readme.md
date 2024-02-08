# Программа для перевода со скриншотов
По задумке автора (меня), эта программа должна помочь переводить манхуа, мангу и т.д., но, в конечном счёте может
переводить практически любой текст со скриншотов

# Установка
Потребуется tesseract, для этого нужно поставить отдельно

Ссылка на [официальный сайт](https://tesseract-ocr.github.io/tessdoc/Installation.html)

## linux

```shell
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Windows

```shell
python3 -m venv venv
source venv\Scripts\activate
pip install -r requirements.txt
```

# Запуск
`python main.py`