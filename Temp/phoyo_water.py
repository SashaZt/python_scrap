from PIL import Image
import os

# указываем путь до папки с изображениями
# path = 'photos_waters'

# создаем папку photos_clean, если ее еще нет
if not os.path.exists("photos_clean"):
    os.makedirs("photos_clean")

# пройдемся по всем файлам в папке photos_waters
for filename in os.listdir("photos_waters"):
    # получаем путь к файлу
    input_path = os.path.join("photos_waters", filename)

    # загружаем изображение
    with Image.open(input_path) as img:
        # получаем размеры изображения
        width, height = img.size

        # создаем пустое изображение такого же размера
        output_img = Image.new(mode="RGB", size=(width, height), color=(255, 255, 255))

        # наложим на него исходное изображение
        output_img.paste(img, (0, 0))

        # сохраним результирующее изображение в папку photos_clean
        output_path = os.path.join("photos_clean", filename)
        output_img.save(output_path)