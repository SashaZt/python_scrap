url = 'https://vehiclebid.info/ru/lots/jf1gpar60e8319811-72288952'
# url = '=IMAGE("https://sortiment.lidl.ch/media/catalog/product/cache/38c728e59b3a47950872534eff8a1e63/2/3/2332_ApfelZimt_PSXX.jpg")'

new_url = url.split("-")[-1]

import glob

targetPattern = f"C:\\scrap_tutorial-master\\vehiclebid_bot\\data\\*.html"
files_html = glob.glob(targetPattern)
for item in files_html:
    if item.split("\\")[-1].replace(".html", "") in url:
        print('YES')
    else:
        print('NOT')

# if "word" in string:
#     print("Found")
# else:
#     print("Not Found")
# print(new_url)
