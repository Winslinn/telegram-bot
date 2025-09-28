import os, threading, asyncio, gettext
import database as db

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from functools import lru_cache

from commands import listen_input
from bot_api import run_api
from translator import translate_message

gettext.bindtextdomain('messages', 'locales')

gettext.textdomain('messages')
_ = gettext.gettext

app = ApplicationBuilder().token(os.environ["BOT_TOKEN"]).build()

def command(cmd):
    def decorator(func):
        app.add_handler(CommandHandler(cmd, func))
    return decorator

@command("start")
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    _ = translate_message(update)
    
    if db.check_user(update) is None:
        await update.message.reply_text(_("Hello 👋! This is a bot that allows you to quickly get news from various news sites. To get started, send a link containing the site's domain name, or use other features of this bot below!"))
        db.add_user(update)
    else:
        await update.message.reply_text(_("🏠Home"))
    
if __name__ == '__main__':
    print("Bot environment initialized. Listening webhook...")
    
    loop = asyncio.get_event_loop()
    
    # Feature initialization
    threading.Thread(target=listen_input, args=(app, loop), daemon=True).start()
    threading.Thread(target=run_api, daemon=True).start()
    
    database, db_cursor = db.init_db()
    
    app.run_webhook(
        listen="0.0.0.0",
        port=3000,
        url_path="webhook",
        webhook_url=os.environ["WEBHOOK"],
        drop_pending_updates=True
    )