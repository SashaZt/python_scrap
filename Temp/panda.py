import time

import pandas as pd
import glob

# files_xlsx = glob.glob("C:\\scrap_tutorial-master\\uniongroup\panda\\*.xlsx")
files_csv = glob.glob("C:\\scrap_tutorial-master\\uniongroup\panda\\*.csv")

# Преоброзование Ексель файла в CSV
# read_file = pd.read_excel("C:\\scrap_tutorial-master\\uniongroup\panda\\price.xlsx")
# read_file.to_csv("C:\\scrap_tutorial-master\\uniongroup\panda\\price.csv",
#                  sep=';',
#                  encoding='cp1251',
#                  index=None,
#                  header=True
#                  )
#
combined = pd.DataFrame()
for file in files_csv:
    data = pd.read_csv(file,sep=';', encoding='cp1251')
    # data = pd.read_excel(file)

    print(data)
# data['filename'] = file.replace(".json", "").split("\\")[-1].replace(" ", "_").replace(".csv", "")
# combined = pd.concat([combined, data])
#
# combined.to_csv(
#     "C:\\scrap_tutorial-master\\uniongroup\panda\\test.csv",
#     encoding='cp1251',
#     index=False,
#     sep=';'
# )
