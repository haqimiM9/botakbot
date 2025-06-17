import os
import requests
import threading
from datetime import datetime
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
GOLDAPI_KEY = os.getenv("GOLDAPI_KEY")

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
        if response.status_code == 200:
            data = response.json()
            spot_price = data["price"]
            timestamp = data["timestamp"]

            price_per_gram = spot_price / 31.1035
            price_24k = round(price_per_gram, 2)
            price_22k = round(price_24k * 0.916, 2)
            price_21k = round(price_24k * 0.875, 2)

            date_str = datetime.fromtimestamp(timestamp).strftime("%d %b %Y %I:%M %p")

            change_24k = -0.04
            change_22k = round(change_24k * 0.916, 2)
            change_21k = round(change_24k * 0.875, 2)

            summary = "📊 Gold price stable – Hold off on buying."

            reply = (
                f"💰 Gold Price Alert (MYR) - {date_str}\n"
                f"Spot Price: RM {spot_price:,.2f}\n"
                f"999.9 (24K): RM {price_24k:,.2f}/g\n"
                f"916 (22K): RM {price_22k:,.2f}/g\n"
                f"21K: RM {price_21k:,.2f}/g\n\n"
                f"📉 Price Change:\n"
                f"24K: {change_24k:+.2f} MYR\n"
                f"22K: {change_22k:+.2f} MYR\n"
                f"21K: {change_21k:+.2f} MYR\n\n"
                f"Summary:\n{summary}"
            )
        else:
            reply = f"❌ Error fetching gold price (Status {response.status_code})"
    except Exception as e:
        reply = f"⚠️ Error: {str(e)}"
    await update.message.reply_text(reply)

def start_bot():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("gold", gold))
    app.run_polling()

# Flask app to keep Render happy
flask_app = Flask(__name__)

@flask_app.route("/")
def index():
    return "Bot is running!", 200

if __name__ == "__main__":
    threading.Thread(target=start_bot).start()
    port = int(os.environ.get("PORT", 10000))
    flask_app.run(host="0.0.0.0", port=port)
