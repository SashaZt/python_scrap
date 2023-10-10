from googletrans import Translator, LANGUAGES

translator = Translator()

def translate_text(text, src_lang, dest_lang):
    translated = translator.translate(text, src=src_lang, dest=dest_lang)
    return translated.text

text_to_translate = "大众 途昂 2021款 380TSI 四驱尊崇豪华版"
translated_text = translate_text(text_to_translate, 'zh-CN', 'en')
print(translated_text)
print(text_to_translate)
