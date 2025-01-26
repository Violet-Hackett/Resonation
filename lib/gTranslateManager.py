from google.cloud import translate_v2 as translate
import json
import languageManager as langm

translate_client = translate.Client()

def translate(english_text: str, target_lang: langm.Language):

    # Check cache
    fp = f'bin/installed_languages/{target_lang.name}/cache/translations.json'
    with open(fp, 'r', encoding='utf-8') as translations_json:
        translations = json.load(translations_json)

    if not english_text in translations.keys():
        #print('API call made (gCloud Translate)')
        translation = translate_client.translate(english_text, target_language=target_lang.abbreviation)['translatedText']
        translations[english_text] = translation
        with open(fp, "w", encoding="utf-8") as translations_json:
            json.dump(translations, translations_json, ensure_ascii=False, indent=4)
        return translation
    return translations[english_text]
