import os
import threading
import requests
from datetime import datetime
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
GOLDAPI_KEY = os.getenv("GOLDAPI_KEY")

# Telegram Bot command handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi, welcome to BotakBot!\nTo get gold price, type /gold")

async def gold(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        url = "https://www.goldapi.io/api/XAU/MYR"
        headers = {
            "x-access-token": GOLDAPI_KEY,
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers)
        data = response.json()
        
        spot_price = data["price"]
        price_per_gram = spot_price / 31.1035
        price_24k = round(price_per_gram, 2)
        price_22k = round(price_24k * 0.916, 2)
        price_21k = round(price_24k * 0.875, 2)

        date_str = datetime.fromtimestamp(data["timestamp"]).strftime("%d %b %Y %I:%M %p")

        reply = (
            f"💰 Gold Price Alert (MYR) - {date_str}\n"
            f"Spot Price: RM {spot_price:,.2f}\n"
            f"999.9 (24K): RM {price_24k:.2f}/g\n"
            f"916 (22K): RM {price_22k:.2f}/g\n"
            f"21K: RM {price_21k:.2f}/g\n\n"
            f"📉 Price Change:\n"
            f"24K: -0.04 MYR\n"
            f"22K: -0.04 MYR\n"
            f"21K: -0.04 MYR\n\n"
            f"Summary:\n📊 Gold price stable – Hold off on buying."
        )

    except Exception as e:
        reply = f"⚠️ Error: {str(e)}"

    await update.message.reply_text(reply)

# Flask app for Render health check
flask_app = Flask(__name__)

@flask_app.route("/")
def index():
    return "BotakBot is running!", 200

# Background thread for Telegram bot
def run_bot():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("gold", gold))
    app.run_polling()

# Start bot in background when Flask starts
if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    port = int(os.environ.get("PORT", 10000))
    flask_app.run(host="0.0.0.0", port=port)
