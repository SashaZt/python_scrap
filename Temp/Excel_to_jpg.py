import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import textwrap

# Читаем файл Excel
df = pd.read_excel('setka.xlsx')
matplotlib.rcParams['font.family'] = 'Garamond'  # Замените  на желаемый шрифт


# Обработка данных для автоматического переноса строки
# max_width = 10 # максимальное количество символов в одной строке
# df = df.applymap(lambda x: textwrap.fill(str(x), max_width))

fig, ax = plt.subplots(figsize=(5, 5))
ax.axis('off')

# Создаем таблицу
table = ax.table(cellText=df.values, colLabels=df.columns, loc='center', cellLoc='center')

# Увеличиваем размер шрифта
table.auto_set_font_size(False)
table.set_fontsize(2)

# Удаляем рамку вокруг таблицы, делаем все границы ячеек белыми
for key, cell in table.get_celld().items():
    cell.set_edgecolor("white")

# Добавляем горизонтальные линии для всех ячеек, не являющихся заголовками
for key, cell in table.get_celld().items():
    if key[0] > 0:
        cell.set_edgecolor("black")
#
# # Регулируем отступы
# plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)

# Сохраняем изображение с высоким разрешением
plt.savefig('setka.jpg', dpi=600, bbox_inches='tight')
