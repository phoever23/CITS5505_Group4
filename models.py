from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    # Need a library like Werkzeug or passlib for hashing later.
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
