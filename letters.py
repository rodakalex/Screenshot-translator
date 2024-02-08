import cv2
import pytesseract

# Загрузка изображения с текстом
image = cv2.imread('screenshot.png')

# Преобразование изображения в оттенки серого
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Применение бинаризации для получения черно-белого изображения
threshold_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# Использование библиотеки pytesseract для распознавания текста
text = pytesseract.image_to_string(threshold_image, config='--psm 6')

# Разбиение текста на символы
characters = list(text)

# Вывод результата
print(''.join(characters))
