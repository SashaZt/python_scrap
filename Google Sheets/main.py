import pandas as pd
# Подключение к API GOOGLE___________________________________________________________________
from pprint import pprint

import googleapiclient
import httplib2
from googleapiclient import discovery
from googleapiclient.http import MediaFileUpload
from oauth2client.service_account import ServiceAccountCredentials


# Файл, полученный в Google Developer Console
CREDENTIALS_FILE = 'lidl.json'
# ID Google Sheets документа (можно взять из его URL)
spreadsheet_id = '1XlJk4x9-o9OiRJLdwSOtv0x4GFxJLja0Hv7oBHPgjMU'

# Авторизуемся и получаем service — экземпляр доступа к API
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = googleapiclient.discovery.build('sheets', 'v4', http = httpAuth)
# Подключение к API GOOGLE___________________________________________________________________
#
#
#

# # Пример чтения файла
# values = service.spreadsheets().values().get(
#     spreadsheetId=spreadsheet_id,
#     range='A1:E10',
#     majorDimension='COLUMNS'
# ).execute()

folder_id = '18x4ih6M9pvzBwClm8'
name = 'product'
file_path = "c:\\scrap_tutorial-master\\Google Sheets\\product.csv"
file_metadata = {
                'name': name,
                'mimeType': 'application/vnd.google-apps.spreadsheet',
                'parents': [folder_id]
            }
media = MediaFileUpload(file_path, mimetype='text/csv', resumable=True)
# Пример записи в файл
file = service.files().create(body=file_metadata, media_body=media,
                              fields='id').execute()






# product = ("c:\\scrap_tutorial-master\\Google Sheets\\product.csv")
# product_dataframe = pd.read_csv(product ,sep=';', encoding='cp1251')
# print(product_dataframe)

# # Пример записи в файл
# values = service.spreadsheets().values().batchUpdate(
#     spreadsheetId=spreadsheet_id,
#     body={
#         "valueInputOption": "USER_ENTERED",
#         "data": [
#             {"range": "B3:C4",
#              "majorDimension": "ROWS",
#              "values": [["This is B3", "This is C3"], ["This is B4", "This is C4"]]}
# 	]
#     }
# ).execute()





# # Пример не удалять
# values = service.spreadsheets().values().batchUpdate(
#     spreadsheetId=spreadsheet_id,
#     body={
#         "valueInputOption": "USER_ENTERED",
#         "data": [
#             {"range": "B3:C4",
#              "majorDimension": "ROWS",
#              "values": [["This is B3", "This is C3"], ["This is B4", "This is C4"]]},
#             {"range": "D5:E6",
#              "majorDimension": "COLUMNS",
#              "values": [["This is D5", "This is D6"], ["This is E5", "=5+5"]]}
# 	]
#     }
# ).execute()