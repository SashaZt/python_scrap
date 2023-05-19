# import aiofiles
# import asyncio
# import aiohttp
# import os
# import json
#
# async def download_image(url, filename, headers):
#     async with aiohttp.ClientSession(headers=headers) as session:
#         async with session.get(url) as response:
#             async with aiofiles.open(filename, "wb") as f:
#                 await f.write(await response.read())
#
# async def main():
#     # загружаем данные из файла JSON
#     async with aiofiles.open("result.json", "r") as json_file:
#         result_dict = json.loads(await json_file.read())
#
#     header = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
#     }
#
#     tasks = []
#     count = 0 # переменная для подсчета количества сохраненных файлов
#
#     # проходимся по каждому элементу словаря
#     for item, item_dict in result_dict.items():
#         url_count = sum(key.startswith("url_") for key in item_dict.keys())
#
#         for i in range(1, url_count + 1):
#             url = item_dict[f"url_{i}"]
#             id_product = item_dict[f"id_{i}"].replace("/", "-")
#             filename = f'c:\\Data_olekmotocykle\\img\\{id_product}.jpg'
#             previous_filename = f'c:\\Data_olekmotocykle\\img\\{id_product}_{i - 1}.jpg'
#
#             if os.path.exists(filename) or (i > 1 and os.path.exists(previous_filename)):
#                 continue
#
#             if i > 1:
#                 filename = previous_filename
#
#             tasks.append(asyncio.create_task(download_image(url, filename, header)))
#             count += 1
#     # for item, item_dict in result_dict.items(): #Убрать срез
#     #     # получаем количество URL-адресов
#     #     url_count = sum(key.startswith("url_") for key in item_dict.keys())
#     #
#     #     # если есть только один URL-адрес
#     #     if url_count == 1:
#     #         url = item_dict["url_1"]
#     #         id_product = item_dict["id_1"].replace("/", "-")
#     #         tasks.append(asyncio.create_task(download_image(url, f'c:\\Data_olekmotocykle\\img\\{id_product}.jpg', header)))
#     #         count += 1
#     #     else:
#     #         # если есть несколько URL-адресов
#     #         for i in range(1, url_count + 1):
#     #             url = item_dict[f"url_{i}"]
#     #             id_product = item_dict[f"id_{i}"].replace("/", "-")
#     #             if i == 1:
#     #                 tasks.append(asyncio.create_task(download_image(url, f'c:\\Data_olekmotocykle\\img\\{id_product}.jpg', header)))
#     #             if i > 1:
#     #                 tasks.append(asyncio.create_task(download_image(url, f'c:\\Data_olekmotocykle\\img\\{id_product}_{i-1}.jpg', header)))
#     #             count += 1
#
#         # проверяем, было ли сохранено 1000 файлов
#         if count % 1000 == 0:
#             print(f'Saved {count} files, waiting 10 seconds...')
#             await asyncio.sleep(30)
#
#     # если остались некоторые необработанные файлы, то сохраняем их
#     if count % 1000 != 0:
#         print(f'Saved {count} files, waiting 10 seconds...')
#         await asyncio.sleep(30)
#
#     await asyncio.gather(*tasks)
#
# asyncio.run(main())

import aiofiles
import asyncio
import aiohttp
import os
import json

async def download_image(url, filename, headers):
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as response:
            async with aiofiles.open(filename, "wb") as f:
                await f.write(await response.read())

async def main():

    async with aiofiles.open("result.json", "r") as json_file:
        result_dict = json.loads(await json_file.read())

    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
    }

    tasks = []
    count = 0  # переменная для подсчета количества сохраненных файлов

    for item, item_dict in result_dict.items():
        url_count = sum(key.startswith("url_") for key in item_dict.keys())

        for i in range(1, url_count + 1):
            url = item_dict[f"url_{i}"]
            id_product = item_dict[f"id_{i}"].replace("/", "-")
            filename = f'c:\\Data_olekmotocykle\\img\\{id_product}.jpg'
            previous_filename = f'c:\\Data_olekmotocykle\\img\\{id_product}_{i - 1}.jpg'

            if os.path.exists(filename) or (i > 1 and os.path.exists(previous_filename)):
                continue

            if i > 1:
                filename = previous_filename

            tasks.append(asyncio.create_task(download_image(url, filename, header)))
            count += 1

            # проверяем, было ли сохранено 1000 файлов
            if count % 1000 == 0:
                print(f'Saved {count} files, waiting 10 seconds...')
                await asyncio.sleep(10)

    # если остались некоторые необработанные файлы, то сохраняем их
    if count % 1000 != 0:
        print(f'Saved {count} files, waiting 10 seconds...')
        await asyncio.sleep(10)

    await asyncio.gather(*tasks)

asyncio.run(main())
