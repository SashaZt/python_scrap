# import json
# import html
#
# # Ваша строка
# data_str = '[{&quot;id&quot;: 1839181479, &quot;url&quot;: &quot;/ua/p1839181479-termoregulyator-dlya-teplogo.html&quot;, &quot;name&quot;: &quot;\\u0422\\u0435\\u0440\\u043c\\u043e\\u0440\\u0435\\u0433\\u0443\\u043b\\u044f\\u0442\\u043e\\u0440 \\u0434\\u043b\\u044f \\u0442\\u0435\\u043f\\u043b\\u043e\\u0457 \\u043f\\u0456\\u0434\\u043b\\u043e\\u0433\\u0438 RTC 70.26 \\u0437 \\u0434\\u0430\\u0442\\u0447\\u0438\\u043a\\u043e\\u043c \\u043f\\u0456\\u0434\\u043b\\u043e\\u0433\\u0438 3 \\u043c\\u0435\\u0442\\u0440\\u0438 \\u0431\\u0456\\u043b\\u0438\\u0439&quot;}, {&quot;id&quot;: 1385598736, &quot;url&quot;: &quot;/ua/p1385598736-133-omm-nagrevatelnyj.html&quot;, &quot;name&quot;: &quot;133 \\u041e\\u043c/\\u043c. \\u041d\\u0430\\u0433\\u0440\\u0435\\u0432\\u0430\\u0442\\u0435\\u043b\\u044c\\u043d\\u044b\\u0439 \\u043a\\u0430\\u0440\\u0431\\u043e\\u043d\\u043e\\u0432\\u044b\\u0439 \\u043a\\u0430\\u0431\\u0435\\u043b\\u044c 3\\u041a \\u0432 \\u0441\\u0438\\u043b\\u0438\\u043a\\u043e\\u043d\\u043e\\u0432\\u043e\\u0439 \\u0438\\u0437\\u043e\\u043b\\u044f\\u0446\\u0438\\u0438&quot;}]'
#
# # Декодирование HTML
# decoded_str = html.unescape(data_str)
#
# # Декодирование JSON
# data = json.loads(decoded_str)
#
# # Теперь data - это список словарей, и вы можете с ним работать
# for item in data:
#     print(f"ID: {item['id']}")
#     print(f"URL: {item['url']}")
#     print(f"Name: {item['name']}")
#
#
#
#
#
# # Создание 32 блоков первого типа
# for i in range(1, 33):
#     block_name = f"goip_{str(i).zfill(2)}"
#     print(f"[{block_name}]")
#     print(f"exten => _X.,1,NoOp(Original dialed number is ${{EXTEN}})")
#     print(f"exten => _X.,n,Set(FinalNumber=7${{EXTEN}})")
#     print(f"exten => _X.,n,Dial(SIP/{block_name}/{i}${{FinalNumber}},60)")
#     print(f"exten => _X.,n,Hangup()")
#     print()

# Создание 32 блоков
for i in range(1, 33):
    block_name = f"goip_{str(i).zfill(2)}"

    print(f"[{block_name}]")

    print("exten => _8XX.,1,NoOp(Original dialed number is ${EXTEN})")
    print(f"exten => _8XX.,n,Set(FinalNumber={i}${{EXTEN}})")
    print(f"exten => _8XX.,n,Dial(SIP/{block_name}/${{FinalNumber}},60)")
    print("exten => _8XX.,n,Hangup()")

    print("exten => _+7X.,1,NoOp(Original dialed number is ${EXTEN})")
    print(f"exten => _+7X.,n,Set(FinalNumber={i}${{EXTEN}})")
    print(f"exten => _+7X.,n,Dial(SIP/{block_name}/8${{FinalNumber:2}},60)")
    print("exten => _+7X.,n,Hangup()")

    print()  # Пустая строка между блоками


# # Генерация 32 блоков
# for i in range(1, 33):
#     block_name = f"goip_{str(i).zfill(2)}"
#
#     print(f"[{block_name}]")
#
#     # Первый тип exten (_8.)
#     print(f"exten => _8.,1,NoOp(Original dialed number is ${{EXTEN}})")
#     print(f"exten => _8.,n,Set(FinalNumber={i}${{EXTEN}})")
#     print(f"exten => _8.,n,Dial(SIP/{block_name}/${{FinalNumber}},60)")
#     print(f"exten => _8.,n,Hangup()")
#
#     # Второй тип exten (_7.)
#     print(f"exten => _7.,1,NoOp(Original dialed number is ${{EXTEN}})")
#     print(f"exten => _7.,n,Set(FinalNumber=8${{EXTEN:1}})")
#     print(f"exten => _7.,n,Dial(SIP/{block_name}/{i}${{FinalNumber}},60)")
#     print(f"exten => _7.,n,Hangup()")
#
#     print()  # Пустая строка между блоками

