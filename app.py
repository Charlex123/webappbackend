from flask import Flask, request, jsonify, make_response
from models import db, User, Referral, Blockchains, Clubs, Country, Managers
from dotenv import load_dotenv
from pathlib import Path
import cloudinary
import cloudinary.uploader
import cloudinary.api
from flask_cors import CORS 
import os
import telebot
import logging

# Setup logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv('DATABASE_URL')
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Configure Cloudinary
cloudinary.config(
    cloud_name = os.getenv('CLOUD_NAME'),
    api_key = os.getenv('CLOUDINARY_API_KEY'),
    api_secret = os.getenv('CLOUDINARY_SECRET_KEY')
)

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
    
# get all blockchains
@app.route('/api/blockchains', methods=['GET'])
def get_blockchains():
  try:
    blkchains = Blockchains.query.all()
    blkchains_data = [{'id': blkchain.id, 'symbol': blkchain.symbol, 'logo' : blkchain.logo, 'points': blkchain.points} for blkchain in blkchains]
    return jsonify(blkchains_data), 200
  except Exception as e:
    return make_response(jsonify({'message': 'error getting blockchains', 'error': str(e)}), 500)

# get all clubs
@app.route('/api/clubs', methods=['GET'])
def get_clubs():
  try:
    clubs = Clubs.query.all()
    clubs_data = [{'id': club.id, 'symbol': club.symbol, 'logo' : club.logo,'points': club.points} for club in clubs]
    return jsonify(clubs_data), 200
  except Exception as e:
    return make_response(jsonify({'message': 'error getting clubs', 'error': str(e)}), 500)

# get all managers
@app.route('/api/managers', methods=['GET'])
def get_managers():
  try:
    managers = Managers.query.all()
    managers_data = [{'id': manager.id, 'symbol': manager.symbol, 'logo' : manager.logo,'points': manager.points} for manager in managers]
    return jsonify(managers_data), 200
  except Exception as e:
    return make_response(jsonify({'message': 'error getting clubs', 'error': str(e)}), 500)
    
# get all countries
@app.route('/api/countries', methods=['GET'])
def get_countries():
  try:
    countries = Country.query.all()
    countries_data = [{'id': country.id, 'symbol': country.symbol, 'logo' : country.logo,'points': country.points} for country in countries]
    return jsonify(countries_data), 200
  except Exception as e:
    return make_response(jsonify({'message': 'error getting clubs', 'error': str(e)}), 500)
    
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

@app.route('/api/blockchain/add', methods=['POST'])
def add_blockchin_route():
    if 'logo' not in request.files:
        return jsonify({'message': 'No blockchain logo file provided'}), 400

    logo = request.files['logo']
    if logo.filename == '':
        return jsonify({'message': 'No selected blockchain logo file'}), 400

    try:
        upload_result = cloudinary.uploader.upload(logo)
        logo_url = upload_result['secure_url']

        data = request.form
        alreadyexists = Blockchains.query.filter_by(name=data['name']).first()
        if alreadyexists:
            return jsonify({'message': 'Blockchain already exists'}), 200
        
        new_blockchain = Blockchains(
            name=data['name'],
            symbol=data['symbol'],
            points=data['points'],
            logo=logo_url
        )
        db.session.add(new_blockchain)
        db.session.commit()
        return jsonify({
            'id': new_blockchain.id,
            'name': new_blockchain.name,
            'symbol': new_blockchain.symbol,
            'logo': new_blockchain.logo,
            'points': new_blockchain.points
        }), 201
    except Exception as e:
        return jsonify({'message': 'Failed to blockchain upload logo', 'error': str(e)}), 500
    
@app.route('/api/update_blockchain/<int:blockchain_id>', methods=['PUT'])
def update_blockchain_route(blockchain_id):
    try:
        blockchain = Blockchains.query.get(blockchain_id)
        if not blockchain:
            return jsonify({'message': 'blockchain not found'}), 404

        data = request.form
        logo_url = blockchain.logo  # Default to existing logo

        # Handle logo upload if a new file is provided
        if 'logo' in request.files:
            logo = request.files['logo']
            if logo.filename != '':
                upload_result = cloudinary.uploader.upload(logo)
                logo_url = upload_result['secure_url']

        # Update blockchain details
        blockchain.name = data.get('name', blockchain.name)
        blockchain.symbol = data.get('symbol', blockchain.symbol)
        blockchain.points = data.get('points', blockchain.points)
        blockchain.logo = logo_url

        db.session.commit()

        return jsonify({
            'id': blockchain.id,
            'name': blockchain.name,
            'symbol': blockchain.symbol,
            'logo': blockchain.logo,
            'points': blockchain.points
        }), 200
    except Exception as e:
        return jsonify({'message': 'Failed to update club', 'error': str(e)}), 500

    
@app.route('/api/club/add', methods=['POST'])
def add_club_route():
    if 'logo' not in request.files:
        return jsonify({'message': 'No club logo file provided'}), 400

    logo = request.files['logo']
    if logo.filename == '':
        return jsonify({'message': 'No selected club logo file'}), 400

    try:
        upload_result = cloudinary.uploader.upload(logo)
        logo_url = upload_result['secure_url']

        data = request.form
        alreadyexists = Clubs.query.filter_by(name=data['name']).first()
        if alreadyexists:
            return jsonify({'message': 'club already exists'}), 200
        
        new_club = Clubs(
            name=data['name'],
            symbol=data['symbol'],
            points=data['points'],
            logo=logo_url
        )
        db.session.add(new_club)
        db.session.commit()
        return jsonify({
            'id': new_club.id,
            'name': new_club.name,
            'symbol': new_club.symbol,
            'logo': new_club.logo,
            'points': new_club.points
        }), 201
    except Exception as e:
        return jsonify({'message': 'Failed to club upload logo', 'error': str(e)}), 500

@app.route('/api/update_club/<int:club_id>', methods=['PUT'])
def update_club_route(club_id):
    try:
        club = Clubs.query.get(club_id)
        if not club:
            return jsonify({'message': 'Club not found'}), 404

        data = request.form
        logo_url = club.logo  # Default to existing logo

        # Handle logo upload if a new file is provided
        if 'logo' in request.files:
            logo = request.files['logo']
            if logo.filename != '':
                upload_result = cloudinary.uploader.upload(logo)
                logo_url = upload_result['secure_url']

        # Update club details
        club.name = data.get('name', club.name)
        club.symbol = data.get('symbol', club.symbol)
        club.points = data.get('points', club.points)
        club.logo = logo_url

        db.session.commit()

        return jsonify({
            'id': club.id,
            'name': club.name,
            'symbol': club.symbol,
            'logo': club.logo,
            'points': club.points
        }), 200
    except Exception as e:
        return jsonify({'message': 'Failed to update club', 'error': str(e)}), 500
    
@app.route('/api/manager/add', methods=['POST'])
def add_manager_route():
    if 'logo' not in request.files:
        return jsonify({'message': 'No manager logo file provided'}), 400

    logo = request.files['logo']
    if logo.filename == '':
        return jsonify({'message': 'No selected manager logo file'}), 400

    try:
        upload_result = cloudinary.uploader.upload(logo)
        logo_url = upload_result['secure_url']

        data = request.form
        alreadyexists = Managers.query.filter_by(name=data['name']).first()
        if alreadyexists:
            return jsonify({'message': 'Manager already exists'}), 200
        
        new_manager = Managers(
            name=data['name'],
            symbol=data['symbol'],
            points=data['points'],
            logo=logo_url
        )
        db.session.add(new_manager)
        db.session.commit()
        return jsonify({
            'id': new_manager.id,
            'name': new_manager.name,
            'symbol': new_manager.symbol,
            'logo': new_manager.logo,
            'points': new_manager.points
        }), 201
    except Exception as e:
        return jsonify({'message': 'Failed to manager upload logo', 'error': str(e)}), 500
    
@app.route('/api/update_manager/<int:manager_id>', methods=['PUT'])
def update_manager_route(manager_id):
    try:
        manager = Managers.query.get(manager_id)
        if not manager:
            return jsonify({'message': 'Manager not found'}), 404

        data = request.form
        logo_url = manager.logo  # Default to existing logo

        # Handle logo upload if a new file is provided
        if 'logo' in request.files:
            logo = request.files['logo']
            if logo.filename != '':
                upload_result = cloudinary.uploader.upload(logo)
                logo_url = upload_result['secure_url']

        # Update club details
        manager.name = data.get('name', manager.name)
        manager.symbol = data.get('symbol', manager.symbol)
        manager.points = data.get('points', manager.points)
        manager.logo = logo_url

        db.session.commit()

        return jsonify({
            'id': manager.id,
            'name': manager.name,
            'symbol': manager.symbol,
            'logo': manager.logo,
            'points': manager.points
        }), 200
    except Exception as e:
        return jsonify({'message': 'Failed to update manager', 'error': str(e)}), 500

    
@app.route('/api/country/add', methods=['POST'])
def add_country_route():
    if 'logo' not in request.files:
        return jsonify({'message': 'No country logo file provided'}), 400

    logo = request.files['logo']
    if logo.filename == '':
        return jsonify({'message': 'No selected country logo file'}), 400

    try:
        upload_result = cloudinary.uploader.upload(logo)
        logo_url = upload_result['secure_url']

        data = request.form
        alreadyexists = Country.query.filter_by(name=data['name']).first()
        if alreadyexists:
            return jsonify({'message': 'Country already exists'}), 200
        
        new_country = Country(
            name=data['name'],
            symbol=data['symbol'],
            points=data['points'],
            logo=logo_url
        )
        db.session.add(new_country)
        db.session.commit()
        return jsonify({
            'id': new_country.id,
            'name': new_country.name,
            'symbol': new_country.symbol,
            'logo': new_country.logo,
            'points': new_country.points
        }), 201
    except Exception as e:
        return jsonify({'message': 'Failed to country upload logo', 'error': str(e)}), 500

    
# update user testnet qualification
@app.route('/api/users/<chat_id>/updatetestnet', methods=['PUT'])
def update_testnet(chat_id):
    try:
        user = User.query.filter_by(chat_id=chat_id).first()
        if user:
            user.testnet = True
            db.session.commit()
            return jsonify({'message': 'testnet updated successfully', 'testnet': user.testnet})
        else:
            return jsonify({'message': 'User not found'}), 404
    except Exception as e:
        logger.error(f"Error updating testnet: {e}")
        return jsonify({'message': 'Internal Server Error'}), 500

@app.route('/api/users/adduser', methods=['POST'])
def add_user_route():
    try:
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
            
        else:
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
    except Exception as e:
        logger.error(f"Error adding new user: {e}")
        return jsonify({'message': 'Internal Server Error'}), 500
    

@app.route('/')
def index():
    return "Welcome to the Web App API!"
# Ensure application context and create database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run()
