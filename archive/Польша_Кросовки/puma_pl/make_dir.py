import os

# Определение функции для создания директории, если ее нет
def make_dir_if_not_exists(path):
    if not os.path.exists(path):
        os.mkdir(path)

# Создание списка групп
groups = ["mezczyzni", "kobiety", "dzieciece"]

# Создание директории csv_data
make_dir_if_not_exists("csv_data")

# Создание директорий внутри csv_data для каждой группы
for group in groups:
    group_dir = os.path.join("csv_data", f"img_{group}")
    make_dir_if_not_exists(group_dir)

# Создание директории csv_url
make_dir_if_not_exists("csv_url")

# Создание директорий внутри csv_url для каждой группы
for group in groups:
    group_dir = os.path.join("csv_url", group)
    make_dir_if_not_exists(group_dir)

# Создание директории data_img
make_dir_if_not_exists("data_img")

# Создание директорий внутри data_img для каждой группы
for group in groups:
    group_dir = os.path.join("data_img", f"img_{group}")
    make_dir_if_not_exists(group_dir)

# Создание директории html_data
make_dir_if_not_exists("html_data")

# Создание директорий внутри html_data для каждой группы
for group in groups:
    group_dir = os.path.join("html_data", group)
    make_dir_if_not_exists(group_dir)

# Создание директории html_product
make_dir_if_not_exists("html_product")

# Создание директорий внутри html_product для каждой группы
for group in groups:
    group_dir = os.path.join("html_product", group)
    make_dir_if_not_exists(group_dir)