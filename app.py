from flask import Flask, request, jsonify
from models import db, User, Referral
from dotenv import load_dotenv
from pathlib import Path
from flask_cors import CORS 
import os
import telebot
import logging

# Setup logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
BOT_TOKEN = os.getenv('BOT_TOKEN')

print(f"BOT_TOKEN: {BOT_TOKEN}")
print(f"DATABASE_URL: {DATABASE_URL}")

if not DATABASE_URL or not BOT_TOKEN:
    raise ValueError("DATABASE_URL or BOT_TOKEN environment variables not set.")

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
db.init_app(app)

bot = telebot.TeleBot(BOT_TOKEN)
bot_username = bot.get_me().username

@app.route('/api/users', methods=['GET'])
def get_users():
    try:
        users = User.query.all()
        user_details = []
        for user in users:
            user_details.append({
                'chat_id': user.chat_id,
                'multiplier': user.multiplier,
                'totalpoints': user.totalpoints,
                'dailypoints': user.dailypoints,
                'dailypointscounter': user.dailypointscounter,
                'exchange': user.exchange,
                'level': user.level,
                'levelpoint': user.levelpoint,
                'ref_count': user.ref_count,
                'referral_link': user.referral_link
            })
        return jsonify(user_details)
    except Exception as e:
        logger.error(f"Error fetching users: {e}")
        return jsonify({'message': 'Internal Server Error'}), 500
    
@app.route('/api/users/<chat_id>', methods=['GET'])
def get_user(chat_id):
    try:
        user = User.query.filter_by(chat_id=chat_id).first()
        if user:
            return jsonify({
                'chat_id': user.chat_id,
                'multiplier': user.multiplier,
                'totalpoints': user.totalpoints,
                'dailypoints': user.dailypoints,
                'dailypointscounter': user.dailypointscounter,
                'exchange': user.exchange,
                'level': user.level,
                'levelpoint': user.levelpoint,
                'ref_count': user.ref_count,
                'referral_link': user.referral_link
            }),200
        return jsonify(message='User not found'), 404
    except Exception as e:
        logger.error(f"Error fetching users: {e}")
        return jsonify({'message': 'Internal Server Error'}), 500
    
@app.route('/api/users/<chat_id>/updatemultiplier', methods=['PUT'])
def update_multiplier(chat_id):
    try:
        user = User.query.filter_by(chat_id=chat_id).first()
        if user:
            data = request.get_json()
            user.multiplier = data['multiplier']
            db.session.commit()
            return jsonify({'message': 'multiplier updated successfully','multiplier': user.multiplier})
        else:
            return jsonify({'message': 'User not found'}), 404
    except Exception as e:
        logger.error(f"Error updating multiplier: {e}")
        return jsonify({'message': 'Internal Server Error'})

@app.route('/api/users/<chat_id>/getmultiplier', methods=['GET'])
def get_user_multiplier(chat_id):
    try:
        user = User.query.filter_by(chat_id=chat_id).first()
        if user:
            return jsonify({'chat_id': user.chat_id, 'multiplier': user.multiplier})
        else:
            return jsonify({'message': 'User not found'}), 404
    except Exception as e:
        logger.error(f"Error getting multiplier: {e}")
        return jsonify({'message': 'Internal Server Error'}), 500

@app.route('/api/users/<chat_id>/updatetotalpoints', methods=['PUT'])
def update_totalpoints(chat_id):
    try:
        user = User.query.filter_by(chat_id=chat_id).first()
        if user:
            data = request.get_json()
            user.totalpoints = data['totalpoints']
            db.session.commit()
            return jsonify({'message': 'total points updated successfully','totalpoints': user.totalpoints})
        else:
            return jsonify({'message': 'User not found'}), 404
    except Exception as e:
        logger.error(f"Error updating total points: {e}")
        return jsonify({'message': 'Internal Server Error'}), 500
    
@app.route('/api/users/<chat_id>/updatedailypoints', methods=['PUT'])
def update_dailypoints(chat_id):
    try:
        user = User.query.filter_by(chat_id=chat_id).first()
        if user:
            data = request.get_json()
            user.dailypoints = data['dailypoints']
            db.session.commit()
            return jsonify({'message': 'daily points updated successfully','dailypoints': user.dailypoints})
        else:
            return jsonify({'message': 'User not found'}), 404
    except Exception as e:
        logger.error(f"Error updating daily points: {e}")
        return jsonify({'message': 'Internal Server Error'}), 500
    
@app.route('/api/users/<chat_id>/updatedailypointscounter', methods=['PUT'])
def update_dailypointscounter(chat_id):
    try:
        user = User.query.filter_by(chat_id=chat_id).first()
        if user:
            data = request.get_json()
            user.dailypointscounter = data['dailypointscounter']
            db.session.commit()
            return jsonify({'message': 'daily points counter updated successfully','dailypointscounter': user.dailypointscounter})
        else:
            return jsonify({'message': 'User not found'}), 404
    except Exception as e:
        logger.error(f"Error updating daily points counter: {e}")
        return jsonify({'message': 'Internal Server Error'}), 500
    
@app.route('/api/users/<chat_id>/gettotalpoints', methods=['GET'])
def get_user_totalpoints(chat_id):
    try:
        user = User.query.filter_by(chat_id=chat_id).first()
        if user:
            return jsonify({'chat_id': user.chat_id, 'totalpoints': user.totalpoints})
        else:
            return jsonify({'message': 'User not found'}), 404
    except Exception as e:
        logger.error(f"Error getting total points: {e}")
        return jsonify({'message': 'Internal Server Error'}), 500
        
@app.route('/api/users/<chat_id>/getdailypoints', methods=['GET'])
def get_user_dailypoints(chat_id):
    try:
        user = User.query.filter_by(chat_id=chat_id).first()
        if user:
            return jsonify({'chat_id': user.chat_id, 'dailypoints': user.dailypoints})
        else:
            return jsonify({'message': 'User not found'}), 404
    except Exception as e:
        logger.error(f"Error getting daily points: {e}")
        return jsonify({'message': 'Internal Server Error'}), 500
    
@app.route('/api/users/<chat_id>/getdailypointscounter', methods=['GET'])
def get_dailypointscounter(chat_id):
    try:
        user = User.query.filter_by(chat_id=chat_id).first()
        if user:
            return jsonify({'chat_id': user.chat_id, 'dailypointscounter': user.dailypointscounter})
        else:
            return jsonify({'message': 'User not found'}), 404
    except Exception as e:
        logger.error(f"Error getting daily points counter: {e}")
        return jsonify({'message': 'Internal Server Error'}), 500
    
@app.route('/api/users/<chat_id>/updateexchange', methods=['PUT'])
def update_exchange(chat_id):
    try:
        user = User.query.filter_by(chat_id=chat_id).first()
        if user:
            data = request.get_json()
            user.exchange = data['exchange']
            db.session.commit()
            return jsonify({'message': 'Exchange updated successfully', 'exchange': user.exchange})
        else:
            return jsonify({'message': 'User not found'}), 404
    except Exception as e:
        logger.error(f"Error updating exchange: {e}")
        return jsonify({'message': 'Internal Server Error'}), 500
    
@app.route('/api/users/<chat_id>/getexchange', methods=['GET'])
def get_exchange(chat_id):
    try:
        user = User.query.filter_by(chat_id=chat_id).first()
        if user:
            return jsonify({'chat_id': user.chat_id, 'exchange': user.exchange})
        else:
            return jsonify({'message': 'User not found'}), 404
    except Exception as e:
        logger.error(f"Error getting exchange: {e}")
        return jsonify({'message': 'Internal Server Error'}), 500

@app.route('/api/users/<chat_id>/updatelevel', methods=['PUT'])
def update_level(chat_id):
    try:
        user = User.query.filter_by(chat_id=chat_id).first()
        if user:
            data = request.get_json()
            user.level = data['level']
            db.session.commit()
            return jsonify({'message': 'Level updated successfully', 'level': user.level})
        else:
            return jsonify({'message': 'User not found'}), 404
    except Exception as e:
        logger.error(f"Error updating level: {e}")
        return jsonify({'message': 'Internal Server Error'}), 500
    
@app.route('/api/users/<chat_id>/getlevelpoint', methods=['PUT'])
def update_levelpoint(chat_id):
    try:
        user = User.query.filter_by(chat_id=chat_id).first()
        if user:
            data = request.get_json()
            user.levelpoint = data['levelpoint']
            db.session.commit()
            return jsonify({'message': 'Level point updated successfully', 'levelpoint': user.levelpoint})
        else:
            return jsonify({'message': 'User not found'}), 404
    except Exception as e:
        logger.error(f"Error updating level point: {e}")
        return jsonify({'message': 'Internal Server Error'}), 500
    
@app.route('/api/users/<chat_id>/level', methods=['GET'])
def get_user_level(chat_id):
    try:
        user = User.query.filter_by(chat_id=chat_id).first()
        if user:
            return jsonify({'chat_id': user.chat_id, 'level': user.level})
        else:
            return jsonify({'message': 'User not found'}), 404
    except Exception as e:
        logger.error(f"Error getting level: {e}")
        return jsonify({'message': 'Internal Server Error'}), 500
    
@app.route('/api/users/<chat_id>/levelpoint', methods=['GET'])
def get_user_levelpoint(chat_id):
    try:
        user = User.query.filter_by(chat_id=chat_id).first()
        if user:
            return jsonify({'chat_id': user.chat_id, 'levelpoint': user.levelpoint})
        else:
            return jsonify({'message': 'User not found'}), 404
    except Exception as e:
        logger.error(f"Error getting level point: {e}")
        return jsonify({'message': 'Internal Server Error'}), 500
    
@app.route('/api/referrals', methods=['GET'])
def get_referrals():
    referrals = Referral.query.all()
    return jsonify([{'user_id': ref.user_id, 'referred_chat_id': ref.referred_chat_id} for ref in referrals])

@app.route('/api/referrals/<chat_id>', methods=['GET'])
def get_referrals_by_chat_id(chat_id):
    try:
        referrals = Referral.query.filter_by(user_id=chat_id).all()
        if referrals:
            referral_details = []
            for ref in referrals:
                user = User.query.filter_by(chat_id=ref.referred_chat_id).first()
                if user:
                    referral_details.append({
                        'user_id': ref.user_id,
                        'referred_chat_id': ref.referred_chat_id,
                        'referred_user_details': {
                            'chat_id': user.chat_id,
                            'multiplier': user.multiplier,
                            'totalpoints': user.totalpoints,
                            'dailypoints': user.dailypoints,
                            'dailypointscounter': user.dailypointscounter,
                            'exchange': user.exchange,
                            'level': user.level,
                            'levelpoint': user.levelpoint,
                            'ref_count': user.ref_count,
                            'referral_link': user.referral_link
                        }
                    })
            return jsonify(referral_details)
        else:
            return jsonify({'message': 'No referrals found for this user'}), 404
    except Exception as e:
        logger.error(f"Error fetching referrals for chat_id {chat_id}: {e}")
        return jsonify({'message': 'Internal Server Error'}), 500


@app.route('/api/users/adduser', methods=['POST'])
def add_user_route():
    data = request.get_json()
    existing_user = User.query.filter_by(chat_id=data['chat_id']).first()
    if existing_user:
        return jsonify({
            'chat_id': existing_user.chat_id,
            'multiplier': existing_user.multiplier,
            'totalpoints': existing_user.totalpoints,
            'dailypoints': existing_user.dailypoints,
            'dailypointscounter': existing_user.dailypointscounter,
            'exchange': existing_user.exchange,
            'level': existing_user.level,
            'levelpoint': existing_user.levelpoint,
            'ref_count': existing_user.ref_count,
            'referral_link': existing_user.referral_link
        }), 200
    referral_link = f"https://t.me/{bot_username}?start={data['chat_id']}"
    new_user = User(
        chat_id=data['chat_id'], 
        referral_link=referral_link,
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({
        'chat_id': new_user.chat_id,
        'exchange': new_user.exchange,
        'multiplier': new_user.multiplier,
        'totalpoints': new_user.totalpoints,
        'dailypoints': new_user.dailypoints,
        'dailypointscounter': new_user.dailypointscounter,
        'level': new_user.level,
        'levelpoint': new_user.levelpoint,
        'ref_count': new_user.ref_count,
        'referral_link': new_user.referral_link
    }), 201

@app.route('/')
def index():
    return "Welcome to the Web App API!"
# Ensure application context and create database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run()
