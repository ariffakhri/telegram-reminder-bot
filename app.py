from flask import Flask, request
from apscheduler.schedulers.background import BackgroundScheduler
from telegram import Bot
import datetime
import os

API_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
USER_ID = os.environ.get("TELEGRAM_USER_ID")

bot = Bot(API_TOKEN)
app = Flask(__name__)
scheduler = BackgroundScheduler()
scheduler.start()

@app.route("/")
def home():
    return "✅ Reminder bot is running!"

@app.route("/remind", methods=["POST"])
def remind():
    data = request.get_json()
    msg = data.get("message", "🔔 Reminder!")
    time_str = data.get("time")  # format: "HH:MM"

    now = datetime.datetime.now()
    try:
        target_time = datetime.datetime.strptime(time_str, "%H:%M").replace(
            year=now.year, month=now.month, day=now.day
        )
        if target_time < now:
            return "⏱️ Time is in the past!", 400

        def send():
            bot.send_message(chat_id=USER_ID, text=f"🔔 Reminder: {msg}")

        scheduler.add_job(send, 'date', run_date=target_time)
        return f"Reminder set for {time_str}", 200

    except Exception as e:
        return f"Error: {e}", 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)