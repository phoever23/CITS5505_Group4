from flask import Flask, render_template, url_for, request, jsonify, redirect, flash, session
from config import Config
from models import db, User, Expense
from flask_migrate import Migrate
import random
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard_page'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        existing_user = User.query.filter_by(username=username).first()
        
        if existing_user:
            flash('Username already exists', 'danger')
        elif password != confirm_password:
            flash('Passwords do not match', 'danger')
        else:
            hashed_password = generate_password_hash(password)
            new_user = User(username=username, password_hash=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully! Please login.', 'success')
            return redirect(url_for('login'))
    
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.clear()  # Clear the session
    session.pop('_flashes', None)  # Clear existing flash messages
    flash('You have been logged out', 'info')  # Set new logout message
    return redirect(url_for('login'))

@app.route('/upload')
def upload_page():
    return render_template('upload.html')

@app.route('/dashboard')
def dashboard_page():
    return render_template('dashboard.html')

@app.route('/share')
def share_page():
    return render_template('share.html')

# API Route - fetch expense data as JSON
@app.route('/api/expenses')
def api_expenses():
    expenses = Expense.query.all()
    result = []
    for exp in expenses:
        result.append({
            'date': exp.date.strftime('%Y-%m-%d'),
            'category': exp.category,
            'subCategory': exp.sub_category,
            'amount': exp.amount,
            'currency': exp.currency
        })
    return jsonify(result)


# Optional: Simple route to seed dummy data directly from browser
@app.route('/seed')
def seed_data():
    user = User.query.filter_by(username='demo_user').first()
    if not user:
        user = User(username='demo_user', password_hash='dummyhash')
        db.session.add(user)
        db.session.commit()

    categories = {
        "Housing": ["rent", "mortgage"],
        "Food": ["grocery", "restaurants"],
        "Shopping": ["clothes", "electronics"],
        "Education": ["tuition", "printing"],
        "Others": ["gifts", "transport", "maintenance"]
    }

    currencies = ["AUD", "GBP", "USD", "CAD", "EUR"]

    for _ in range(50):
        cat = random.choice(list(categories.keys()))
        sub = random.choice(categories[cat])
        exp = Expense(
            date=datetime.strptime(f"2024-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}", '%Y-%m-%d'),
            category=cat,
            sub_category=sub,
            amount=round(random.uniform(10, 500), 2),
            currency=random.choice(currencies),
            author=user
        )
        db.session.add(exp)

    db.session.commit()
    return 'Dummy data inserted! Go to /dashboard now.'

if __name__ == '__main__':
    app.run(debug=True)