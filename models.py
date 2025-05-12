from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    # Relationship: A user can have many expenses
    expenses = db.relationship('Expense', backref='author', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.username}>'

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow, nullable=False)
    category = db.Column(db.String(64), index=True, nullable=False)
    sub_category = db.Column(db.String(64), index=True, nullable=True)  
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), nullable=False, default='AUD') 
    # Foreign Key linking to the User table's id column
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Expense {self.category}/{self.sub_category} - {self.amount} {self.currency}>'

class SharedExpense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    shared_by_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    shared_with_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    data_type = db.Column(db.String(20), nullable=False)  # 'all' or 'summary'
    categories = db.Column(db.String(200), nullable=True)  # JSON string of selected categories
    start_date = db.Column(db.DateTime, nullable=True)
    end_date = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    shared_by = db.relationship('User', foreign_keys=[shared_by_id], backref='shared_expenses')
    shared_with = db.relationship('User', foreign_keys=[shared_with_id], backref='received_expenses')
