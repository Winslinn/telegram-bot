import gettext, os

from telegram import Update
from functools import lru_cache

class Translator:
    def __init__(self):
        locales_path = os.path.expanduser('~/bot/locales')
        self.translations = {}
        
        for f in os.listdir(locales_path):
            path = os.path.join(locales_path, f)
            if os.path.isdir(path):
                mo_path = os.path.join(locales_path, f, 'LC_MESSAGES', 'messages.mo')
                with open(mo_path, 'rb') as mo_file:
                    self.translations[f] = gettext.GNUTranslations(mo_file)
        
    @lru_cache(maxsize=100)
    def translate(self, lang_code='en'):
        if self.translations.get(lang_code) is None:
            lang_code = 'en'
        return self.translations[lang_code].gettext
    
translator = Translator()

def translate_message(update: Update):
    user_lang = update.message.from_user.language_code
    return translator.translate(user_lang)