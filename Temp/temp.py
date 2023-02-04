import glob
from datetime import datetime
import re

# str_ = 'Светильник потолочный MAYTONI 43265 (C032CL-L32MG3K) в стиле модерн ➤ Цвет: золото, белый ✈ БЕСПЛАТНАЯ ДОСТАВКА ✈ Киев и вся Украина: ✓ Одесса ✓ Харьков ✓ Днепр ✓ Львов'
url = 'https://www.bcautoencheres.fr/Lot?id=19346880&ItemId=58bffd67-1f4a-4570-b473-2cee37bb131a&q=&bq=saleid_exact%3A15b740e5-49bc-4e22-9c39-7470049e6f22&sort=LotNumber&missingMileage=True&awaitingAppraisal=True&page=1&extraFiltersActive=true&saleHeader=true&returnTo=2-XGJ-79&promoAppliedSets=&R=15&SR=10&SourceSystem=PEEP'
# # url = '=IMAGE("https://sortiment.lidl.ch/media/catalog/product/cache/38c728e59b3a47950872534eff8a1e63/2/3/2332_ApfelZimt_PSXX.jpg")'
# #
# print(re.search(r"[(\d{8})]"), url)

# new_url = url.split("https://www.bcautoencheres.fr/Lot?id=")
# ttt = re.search(r"(\w+)-(\w+)", str_).group(0)
# print(new_url)

path = r'C:\\scrap_tutorial-master\\flagma.ua\\urls_card_01.json'
files = path.replace(".json", "").strip('\\')[-12:]
print(files)

#
#
# targetPattern = f"C:\\scrap_tutorial-master\\vehiclebid_bot\\data\\*.html"
# files_html = glob.glob(targetPattern)
# for item in files_html:
#     if item.split("\\")[-1].replace(".html", "") in url:
#         print('YES')
#     else:
#         print('NOT')

# t = "Лампа в комплекте: Нет лампы"
# regex_ch_08 = 'Лампа'
# if regex_ch_08 in t:
#     print('+')
# else:
#     print("-")
