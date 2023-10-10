import csv
with open('+.csv', 'r', newline='', encoding='utf-8') as file:
    # Создаем объект reader для чтения CSV
    reader = csv.reader(file, delimiter=';')
# Читаем содержимое CSV-файла и обрабатываем каждую строку
    for row in reader:
        # Получаем значения столбцов, используя индексы
        col1 = row[5]  # Значение первого столбца
        col2 = row[1]  # Значение второго столбца
        col3 = row[2]  # Значение третьего столбца

        # Далее можно выполнять нужные операции с полученными значениями столбцов
        # Например, можно фильтровать номера по заданным шаблонам

        # Пример фильтрации номеров по шаблону "+99890"
        if col1.startswith('+99890'):
            print(col1)

        # # Пример фильтрации номеров по шаблону "+99891"
        # if col1.startswith('+99891'):
        #     print(col1)
        #
        # # Пример фильтрации номеров по шаблону "+99893"
        # if col1.startswith('+99893'):
        #     print(col1)





# открываем файл на чтение
with open("input.txt", "r") as input_file:
    # читаем все строки в список
    lines = input_file.readlines()

# создаем список для номеров, которые подходят под шаблон
phone_numbers = []

# проходим по каждой строке
for line in lines:
    # убираем пробелы, скобки и переносы строк
    line = line.replace(" ", "").replace("-", "").replace("(", "").replace(")", "").strip()

    # проверяем, начинается ли номер с нужного кода
    if line.startswith("+99890"):
        phone_numbers.append(line)
    elif line.startswith("+99891"):
        phone_numbers.append(line)
    elif line.startswith("+99893"):
        phone_numbers.append(line)
    elif line.startswith("+99894"):
        phone_numbers.append(line)
    elif line.startswith("+99895"):
        phone_numbers.append(line)
    elif line.startswith("+99897"):
        phone_numbers.append(line)
    elif line.startswith("+99898"):
        phone_numbers.append(line)
    elif line.startswith("+99899"):
        phone_numbers.append(line)
    elif line.startswith("+99833"):
        phone_numbers.append(line)
    # elif line.startswith("+99891"):
    #     phone_numbers.append(line)
    # elif line.startswith("+99892"):
    #     phone_numbers.append(line)
    # elif line.startswith("+99893"):
    #     phone_numbers.append(line)
    # elif line.startswith("+99894"):
    #     phone_numbers.append(line)
    # elif line.startswith("+99895"):
    #     phone_numbers.append(line)
    # elif line.startswith("+99897"):
    #     phone_numbers.append(line)
    # elif line.startswith("+99898"):
    #     phone_numbers.append(line)
    # elif line.startswith("+99899"):
    #     phone_numbers.append(line)
    # elif line.startswith("+998933"):
    #     phone_numbers.append(line)

# открываем файл на запись
with open("output.txt", "w") as output_file:
    # записываем список номеров в файл
    output_file.write("\n".join(phone_numbers))