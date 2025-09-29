import gettext, os

from telegram import Update
from functools import lru_cache

class Translator:
    def __init__(self):
        locales_path = os.path.expanduser('~/bot/locales')
        self.translations = {}
        
        for f in os.listdir(locales_path):
            path = os.path.join(locales_path, f) # Full path to the locale
            if os.path.isdir(path): # Check if it's a directory
                mo_path = os.path.join(locales_path, f, 'LC_MESSAGES', 'messages.mo') # Assuming 'messages.mo' is the domain
                with open(mo_path, 'rb') as mo_file:
                    self.translations[f] = gettext.GNUTranslations(mo_file) # Load the .mo file
        
    @lru_cache(maxsize=100) # Cache up to 100 different language translations
    def translate(self, lang_code='en'):
        if self.translations.get(lang_code) is None:
            lang_code = 'en'
        return self.translations[lang_code].gettext
    
translator = Translator()

def translate_message(update: Update):
    user_lang = update.effective_user.language_code
    return translator.translate(user_lang)