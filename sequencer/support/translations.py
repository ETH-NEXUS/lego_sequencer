import os
import json

TRANSLATIONS_DIR = os.path.join(os.path.dirname(__file__), '../translations')
LANGS = ['en', 'de-CH']

translations = {}
for lang in LANGS:
    # Load main translations
    with open(os.path.join(TRANSLATIONS_DIR, f"{lang}.json"), encoding='utf-8') as f:
        translations[lang] = json.load(f)
    # Load funfacts if available and add to dict
    funfacts_path = os.path.join(TRANSLATIONS_DIR, f"funfacts_{lang}.json")
    if os.path.exists(funfacts_path):
        with open(funfacts_path, encoding='utf-8') as ff:
            translations[lang]['funfacts'] = json.load(ff)


def get_translation(key, lang='en'):
    """
    Supports nested keys with dot notation, e.g. 'reflection_template.general'
    """
    d = translations.get(lang, translations['en'])
    for part in key.split('.'):
        if isinstance(d, dict) and part in d:
            d = d[part]
        else:
            return key  # fallback to key if not found
    return d