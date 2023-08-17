import piexif
image_path = "C:\\scrap_tutorial-master\\Temp\\036_BOSCH_02.jpg"
output_image_path = "C:\\scrap_tutorial-master\\Temp\\036_BOSCH_02_new.jpg"

# Загрузить EXIF данные из изображения
exif_dict = piexif.load(image_path)

# Добавить или изменить метаданные
exif_dict['0th'][piexif.ImageIFD.ImageDescription] = "intercars"
exif_dict['Exif'][piexif.ExifIFD.UserComment] = b"ASCII\0\0\0intercars"

# Конвертировать словарь обратно в байты
exif_bytes = piexif.dump(exif_dict)

# Записать обратно в изображение
piexif.insert(exif_bytes, image_path, output_image_path)