import pandas as pd
import glob

# Преоброзование Ексель файла в CSV
# read_file = pd.read_excel("C:\\scrap_tutorial-master\\uniongroup\\panda\\price_temp.xlsx")
# read_file.to_csv("C:\\scrap_tutorial-master\\uniongroup\\panda\\price.csv",
#                  sep=';',
#                  encoding='cp1251',
#                  index=None,
#                  header=True
#                  )

# Конвертация CSV в  XLSX, читаем csv с необходимыми параметрами, а уже только потом записываев в XLSX
csv = pd.read_csv('2023-01-18_product.csv', sep=';')
excel = pd.ExcelWriter('2023-01-18_product.xlsx')
csv.to_excel(excel)
excel.save()


# # объединение нескольких файлов в один___________________________________________________________
# # Пути к файлам
# # files_xlsx = glob.glob("C:\\scrap_tutorial-master\\uniongroup\\panda\\*.xlsx")
# files_csv = glob.glob("C:\\scrap_tutorial-master\\uniongroup\\data\\*.csv")
# combined = pd.DataFrame()
# for file in files_csv:
#     data = pd.read_csv(file,sep=';', encoding='cp1251')
#     # Добавка значения имени файла в колонку
#     data['filename'] = file.replace(".json", "").split("\\")[-1].replace(" ", "_").replace(".csv", "")
#     combined = pd.concat([combined, data])
#
# combined.to_csv(
#     "C:\\scrap_tutorial-master\\uniongroup\\data\\test.csv",
#     encoding='cp1251',
#     index=False,
#     sep=';'
# )
# # объединение нескольких файлов в один___________________________________________________________


# # объединение двух файлов по колонке card_code_____________________________________________________
# price_file = ("C:\\scrap_tutorial-master\\uniongroup\\data\\price.csv")
# all_file = ("C:\\scrap_tutorial-master\\uniongroup\\data\\all.csv")
# price_dataframe = pd.read_csv(price_file ,sep=';', encoding='cp1251')
# all_dataframe = pd.read_csv(all_file ,sep=';', encoding='cp1251')
# merge_dataframe = price_dataframe.merge(all_dataframe, on=['card_code'])
# merge_dataframe.to_csv(
#     "C:\\scrap_tutorial-master\\uniongroup\\data\\prom.csv",
#     encoding='cp1251',
#     index=False,
#     sep=';'
# )
# # объединение двух файлов по колонке card_code_____________________________________________________

# объединение двух файлов_____________________________________________________
# price_file = ("C:\\scrap_tutorial-master\\uniongroup\\data\\price.csv")
# all_file = ("C:\\scrap_tutorial-master\\uniongroup\\data\\all.csv")
# price_dataframe = pd.read_csv(price_file ,sep=';', encoding='cp1251')
# all_dataframe = pd.read_csv(all_file ,sep=';', encoding='cp1251')
# concat_dataframe = pd.concat([all_dataframe,price_dataframe], axis=1)
# concat_dataframe.to_csv(
#     "C:\\scrap_tutorial-master\\uniongroup\\data\\prom_concat.csv",
#     encoding='cp1251',
#     index=False,
#     sep=';'
# )
# объединение двух файлов_____________________________________________________