import os, threading, asyncio, gettext, requests
import database as db

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler, MessageHandler, filters

from commands import listen_input
from bot_api import run_api
from translator import translate_message

gettext.bindtextdomain('messages', 'locales') # Specify the directory for translation files

gettext.textdomain('messages') # Specify the domain to use, usually the name of the .mo file
_ = gettext.gettext # Alias for easier translation calls

app = ApplicationBuilder().token(os.environ["BOT_TOKEN"]).build()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

def command(cmd): # Decorator to register command handlers
    def decorator(func):
        app.add_handler(CommandHandler(cmd, func))
    return decorator

def main_keyboard(_): # _ is the translation function
    keyboard = [
        [InlineKeyboardButton(_("📰 Get last news"), callback_data="get_news")],
        [InlineKeyboardButton(_("👍 Subscribe to the source"), callback_data="sub_url")],
        [InlineKeyboardButton(_("⚙️ Settings"), callback_data="settings")]
    ]
    return InlineKeyboardMarkup(keyboard)

def start_keyboard(_): # _ is the translation function
    keyboard = [
        [InlineKeyboardButton(_("👍 Subscribe to the source"), callback_data="sub_url")],
        [InlineKeyboardButton(_("ℹ️ Available sources"), callback_data="get_urls")]
    ]
    return InlineKeyboardMarkup(keyboard)

def cancel_input(_):
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton(_("Cancel"), callback_data="cancel_input")]]
    )

@command("start")
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    _ = translate_message(update) # Get the translation function based on user's language
    
    if db.user_subscribed(update):
        await update.message.reply_text(_("🏠 Home"), reply_markup=main_keyboard(_))
    else:
        await update.message.reply_text(_("welcome_message"), reply_markup=start_keyboard(_))
        db.add_user(update)
        
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer() # WARNING! DO NOT REMOVE THIS LINE, IT'S REQUIRED BY TELEGRAM API!!! IT CONFIRMS THAT THE CALLBACK QUERY WAS RECEIVED!!!
    
    data = query.data
    _ = translate_message(update) # Get the translation function based on user's language
    
    # subscribe to URL
    if data == "sub_url":
        id = update.effective_chat.id
        await context.bot.send_message(
            chat_id=id, 
            text=_("Please submit the URL you want to subscribe to (e.g. https://example.com):"),
            reply_markup=cancel_input(_)
        )
        context.user_data["await_input"] = "sub_url" # Set the user state to await URL input
    elif data == "cancel_input":
        await query.delete_message() # Delete the message with the cancel button
        context.user_data["await_input"] = None # Clear the user state

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await_input = context.user_data.get("await_input") # Retrieve the user state of awaiting input
    
    # If the user is expected to input a URL
    if await_input == "sub_url":
        url = update.effective_message.text
        try:
            request = requests.head(url, headers=headers, timeout=10, allow_redirects=True)
            if request.status_code == 200:
                context.user_data["await_input"] = None
                db.user_subscribe_url(update.effective_user.id, url)
                await update.message.reply_text(_("You have subscribed to the URL: {}".format(url)))
            else:
                await update.message.reply_text(_("The URL seems to be invalid. Please try again."))
        except Exception as e:
            await update.message.reply_text(_("Probably this is not a url. Please try again url e.g. https://example.com:"))
            return
    
if __name__ == '__main__':
    print("Bot environment initialized. Listening webhook...")
    
    app.add_handler(CallbackQueryHandler(button_handler)) # Handle button presses
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)) # Handle text messages that are not commands
    
    loop = asyncio.get_event_loop() # Get the current event loop for managing async tasks
    
    # Feature initialization
    threading.Thread(target=listen_input, args=(app, loop), daemon=True).start() # Listen for termimal input
    threading.Thread(target=run_api, daemon=True).start() # Run API server
    
    database, db_cursor = db.init_db()
    
    app.run_webhook(
        listen="0.0.0.0",
        port=3000,
        url_path="webhook",
        webhook_url=os.environ["WEBHOOK"],
        drop_pending_updates=True
    )