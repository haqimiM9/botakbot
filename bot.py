import os
import requests
import asyncio
from datetime import datetime
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
GOLDAPI_KEY = os.getenv("GOLDAPI_KEY")

# Telegram commands
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

# Flask app for Render
flask_app = Flask(__name__)

@flask_app.route("/")
def index():
    return "Bot is running!", 200

# Async runner for both Flask and Telegram
async def run():
    # Start Telegram bot
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("gold", gold))

    # Run bot polling (non-blocking)
    asyncio.create_task(app.run_polling())

    # Run Flask web server
    port = int(os.environ.get("PORT", 10000))
    from hypercorn.asyncio import serve
    from hypercorn.config import Config

    config = Config()
    config.bind = [f"0.0.0.0:{port}"]
    await serve(flask_app, config)

# Start the async runner
if __name__ == "__main__":
    asyncio.run(run())
