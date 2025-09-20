import psutil, os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello!")

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    process = psutil.Process()
    mem_info = process.memory_info().rss / (1024 * 1024)
    message = "{:.2f} MB пам'яті.".format(mem_info) + f"\nСервер запущений: {os.popen('uptime -p').read()[:-1]}"
    await update.message.reply_text("Наразі бот використовує:\n" + message)

if __name__ == '__main__':
    app = ApplicationBuilder().token(os.environ["BOT_TOKEN"]).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("info", info))
    
    print("Starting webhook server")
    app.run_webhook(
        listen="0.0.0.0",
        port=3000,
        url_path="webhook",
        webhook_url=os.environ["WEBHOOK"],
        drop_pending_updates=True
    )
    print("Server started")