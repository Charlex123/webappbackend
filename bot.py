import telebot
from dotenv import load_dotenv
from pathlib import Path
import os
import logging
from flask import Flask
from models import db, User, Referral
import signal
import time
import requests

# Setup logging
logging.basicConfig(level=logging.DEBUG)
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

DATABASE_URL = os.getenv('DATABASE_URL')
BOT_TOKEN = os.getenv('BOT_TOKEN')

if not BOT_TOKEN or not DATABASE_URL:
    raise ValueError("BOT_TOKEN or DATABASE_URL environment variables not set.")

bot = telebot.TeleBot(BOT_TOKEN)

# Setup Flask app context for SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
db.init_app(app)

with app.app_context():
    db.create_all()

def add_user(username, chat_id):
    with app.app_context():
        user = User.query.filter_by(chat_id=str(chat_id)).first()
        if not user:
            referral_link = f"https://t.me/{bot.get_me().username}?start={chat_id}"
            user = User(chat_id=str(chat_id), referral_link=referral_link)
            db.session.add(user)
            db.session.commit()
        return user

def add_referral(referrer_id, referred_chat_id):
    with app.app_context():
        referral = Referral(user_id=referrer_id, referred_chat_id=str(referred_chat_id))
        db.session.add(referral)
        db.session.commit()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    logging.debug("Received start command")
    args = message.text.split()
    chat_id = message.chat.id
    username = message.from_user.username
    user = add_user(username, chat_id)

    if len(args) > 1:
        ref_id = args[1]
        if ref_id != str(chat_id):
            referrer = User.query.filter_by(chat_id=ref_id).first()
            if referrer:
                add_referral(referrer.id, chat_id)

    bot.reply_to(message, f"Hi! Your data has been saved. Your referral link is {user.referral_link}")

@bot.message_handler(commands=['points'])
def get_points(message):
    with app.app_context():
        user = User.query.filter_by(chat_id=str(message.chat.id)).first()
        if user:
            bot.reply_to(message, f"You have {user.points} points.")
        else:
            bot.reply_to(message, "User not found.")

@bot.message_handler(commands=['refer'])
def refer_user(message):
    with app.app_context():
        ref_id = message.text.split()[1]
        referrer = User.query.filter_by(chat_id=str(message.chat.id)).first()
        if referrer:
            referral = Referral(user_id=referrer.id, referred_chat_id=ref_id)
            db.session.add(referral)
            db.session.commit()
            bot.reply_to(message, f"You referred user with chat ID {ref_id}.")
        else:
            bot.reply_to(message, "User not found.")

def run_bot():
    def handle_shutdown(signum, frame):
        print(f"Signal {signum} received, shutting down...")
        bot.stop_polling()

    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, handle_shutdown)
    signal.signal(signal.SIGTERM, handle_shutdown)

    while True:
        try:
            # Start infinite polling with timeout settings
            bot.infinity_polling(timeout=10, long_polling_timeout=5)
        except requests.exceptions.ReadTimeout:
            print("Read timeout occurred. Retrying in 15 seconds...")
            time.sleep(15)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            time.sleep(15)

if __name__ == '__main__':
    run_bot()
