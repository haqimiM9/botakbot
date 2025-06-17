from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from flask import Flask
import threading
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

# --- Telegram Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi, welcome to BotakBot!\nTo get gold price, type /gold")

async def gold(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🪙 Current gold price: (coming soon...)")

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"You said: {update.message.text}")

def start_bot():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("gold", gold))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))
    print("Bot is running...")
    app.run_polling()

# --- Flask Web Server for Render ---
flask_app = Flask(__name__)

@flask_app.route("/")
def index():
    return "Bot is running!", 200

if __name__ == "__main__":
    # Start the Telegram bot in a separate thread
    bot_thread = threading.Thread(target=start_bot)
    bot_thread.start()

    # Start the Flask server (Render expects this)
    port = int(os.environ.get("PORT", 10000))
    flask_app.run(host="0.0.0.0", port=port)
