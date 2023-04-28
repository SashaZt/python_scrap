from PIL import Image
from PIL import ImageGrab
import pytesseract
import time
from datetime import datetime

def main():
    # установка пути к Tesseract OCR в Windows
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    while True:
        # создание скриншота экрана
        screenshot = ImageGrab.grab()

        # сохранение скриншота в файл
        current_time = datetime.now().strftime("%d.%m.%Y_%H_%M")
        filename = f"{current_time}.png"
        screenshot.save(filename)

        # открытие скриншота
        image = Image.open(filename)
        

        # установка области для распознавания текста
        text_area = (540, 130, 630, 500)

        # вырезание области изображения
        cropped_image = image.crop(text_area)
        # Сохраняем 
        cropped_image.save("cropped_image.png")
        
        # распознавание текста с помощью Tesseract OCR
        text = pytesseract.image_to_string(cropped_image, lang='rus')

        # вывод распознанного текста в консоль
        # print(text)

        # сохранение распознанного текста в текстовый файл
        filename = f"{current_time}.txt"
        with open(filename, "w") as f:
            f.write(text)

        # ожидание 5 минут
        time.sleep(300)

if __name__ == '__main__':
    main()