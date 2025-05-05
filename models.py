from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize db instance (usually done in your app factory or __init__.py)
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    # Relationship: A user can have many expenses
    expenses = db.relationship('Expense', backref='author', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.username}>'

class Expense(db.Model):
    __tablename__ = 'expense'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, index=True, default=datetime.utcnow, nullable=False)
    category = db.Column(db.String(64), index=True, nullable=False)
    sub_category = db.Column(db.String(64), index=True, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), nullable=False, default='AUD')

    # Foreign key link to User table
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Expense {self.category}/{self.sub_category} - {self.amount} {self.currency}>'
