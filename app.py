from flask import Flask, render_template, request, jsonify
from models import db, User, Expense
from datetime import datetime
import random

app = Flask(__name__)

# Database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # You can change site.db to anything you want
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Create tables
with app.app_context():
    db.create_all()


# 1. Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload')
def upload_page():
    return render_template('upload.html')

@app.route('/dashboard')
def dashboard_page():
    return render_template('dashboard.html')

@app.route('/share')
def share_page():
    return render_template('share.html')


# 2. API Route - fetch expense data as JSON
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
