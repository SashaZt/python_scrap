import os
import shutil

folder_path = "c:/Users/Administrator/AppData/Local/Temp/"

# Проверяем, существует ли директория
if os.path.exists(folder_path):
    # Удаляем все содержимое директории
    shutil.rmtree(folder_path)
    # Создаем директорию заново
    os.makedirs(folder_path)
else:
    print("Указанная директория не найдена.")
