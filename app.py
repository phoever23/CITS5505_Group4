from flask import Flask, render_template, url_for, request, jsonify, flash
from config import Config
from models import db, User, Expense
from flask_migrate import Migrate
import random
from datetime import datetime
import io
import csv

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_page():
    if request.method == 'POST':
        formData = request.get_json()
        print(formData)
        if all(attr in formData for attr in ('date', 'category', 'subcategory', 'amount', 'currency')):
            try:
                date = datetime.strptime(formData['date'], '%Y-%m-%d')
                category = formData['category']
                sub_category = formData['subcategory']
                amount = float(formData['amount'])
                currency = formData['currency'].upper()
                user_id = 991 # Hardcoded for now replace with current user ID from session

                new_expense = Expense(
                    date=date,
                    category=category,
                    sub_category=sub_category,
                    amount=amount,
                    currency=currency,
                    user_id=user_id
                )
                db.session.add(new_expense)
                db.session.commit()
                return jsonify({
                    'status': 'success',
                    'message':'Manual entry added successfully'
                }), 200
            except ValueError as e:
                return jsonify({
                    'status':'error',
                    'message': f'Invalid data format: {str(e)}'
                }), 400
            except Exception as e:
                db.session.rollback()
                return jsonify({
                    'status':'error',
                    'message':f'Error saving manual entry: {str(e)}'
                }), 500
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
        dummy_user = User(id='991', username='Niranjan', password_hash='sdlkjf439053kjn')
        db.session.add(user)
        db.session.add(dummy_user)
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