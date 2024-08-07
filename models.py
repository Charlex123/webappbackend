from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone


db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.BigInteger, unique=True, nullable=False)
    level = db.Column(db.String(80), default='starter', nullable=False)
    levelpoint = db.Column(db.Integer, default=0)
    exchange = db.Column(db.String(180), default='Binance')
    testnet = db.Column(db.Boolean, default=False)
    multiplier = db.Column(db.Integer, default=5)
    dailypoints = db.Column(db.Integer, default=5000)
    dailypointscounter = db.Column(db.Integer, default=5000)
    ref_count = db.Column(db.Integer, default=0)
    totalpoints = db.Column(db.Integer, default=5000)
    referral_link = db.Column(db.String(250), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now(timezone.utc))

class Referral(db.Model):
    __tablename__ = 'referrals'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id'), nullable=False)
    referred_chat_id = db.Column(db.BigInteger, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now(timezone.utc))

class Blockchains(db.Model):
    __tablename__ = 'blockchains'
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(120), nullable=False)
    symbol = db.Column(db.String(60), nullable=False)
    logo = db.Column(db.String(255), nullable=True)
    points = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    
class Clubs(db.Model):
    __tablename__ = 'clubs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    symbol = db.Column(db.String(60), nullable=False)
    logo = db.Column(db.String(255), nullable=True)
    points = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    
class Managers(db.Model):
    __tablename__ = 'managers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    symbol = db.Column(db.String(60), nullable=False)
    points = db.Column(db.Integer, nullable=False)
    logo = db.Column(db.String(255), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.now(timezone.utc))

class Country(db.Model):
    __tablename__ = 'country'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    symbol = db.Column(db.String(60), nullable=False)
    points = db.Column(db.Integer, nullable=False)
    logo = db.Column(db.String(255), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.now(timezone.utc))