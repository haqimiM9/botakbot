from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_message = (
        "Hi, welcome to BotakBot!\n"
        "To get gold price, type /gold"
    )
    await update.message.reply_text(welcome_message)

# /gold command (dummy response for now)
async def gold(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🪙 Current gold price: (coming soon...)")

# fallback echo for all text messages
async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"You said: {update.message.text}")

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("gold", gold))  # new /gold command
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
