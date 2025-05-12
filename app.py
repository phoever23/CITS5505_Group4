from flask import Flask, render_template, url_for, request, jsonify, redirect, flash, session
from config import Config
from models import db, User, Expense, SharedExpense
from forms import LoginForm, SignupForm
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import io
import csv
import json
from sqlalchemy import String

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard_page'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard_page'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard_page'))
    
    form = SignupForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('signup.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    # Clear any existing flash messages
    session.pop('_flashes', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_page():
    if request.method == 'POST':
        if request.content_type == 'application/json':
            formData = request.get_json()
            if all(attr in formData for attr in ('date', 'category', 'subcategory', 'amount', 'currency')):
                try:
                    date = datetime.strptime(formData['date'], '%Y-%m-%d')
                    category = formData['category']
                    sub_category = formData['subcategory']
                    amount = float(formData['amount'])
                    currency = formData['currency'].upper()
                    
                    new_expense = Expense(
                        date=date,
                        category=category,
                        sub_category=sub_category,
                        amount=amount,
                        currency=currency,
                        user_id=current_user.id
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
        elif 'file' in request.files:
            file = request.files['file']
            if file.filename.endswith('.csv'):
                try:
                    stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
                    reader = csv.DictReader(stream)
                    expenses = []
                    for row in reader:
                        try:
                            expense = Expense(
                                date=datetime.strptime(row['Date'], '%Y-%m-%d'),
                                category=row['Category'],
                                sub_category=row['Sub-category'],
                                amount=float(row['Amount']),
                                currency=row['Currency'].upper(),
                                user_id=current_user.id
                            )
                            expenses.append(expense)
                        except Exception as row_error:
                            return jsonify({
                                'status':'error',
                                'message':f'Invalid row data: {str(row_error)}'
                            }), 400
                    db.session.bulk_save_objects(expenses)
                    db.session.commit()
                    return jsonify({
                        'status': 'success',
                        'message':'CSV uploaded successfully'
                    }), 200
                except Exception as e:
                    db.session.rollback()
                    return jsonify({
                        'status':'error',
                        'message':'CSV upload failed'
                    }), 500
            else:
                return jsonify({
                    'status':'error',
                    'message':'Only CSV files are supported'
                }), 400
        else:
            return jsonify({
                'status':'error',
                'message':'Unsupported content type'
            }), 415
    return render_template('upload.html')

@app.route('/dashboard')
@login_required
def dashboard_page():
    return render_template('dashboard.html')

@app.route('/share')
def share_page():
    return render_template('share.html')

# API Route - fetch expense data as JSON
@app.route('/api/expenses')
@login_required
def api_expenses():
    # Get expenses only for the current user
    expenses = Expense.query.filter_by(user_id=current_user.id).all()
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

@app.route('/api/search-users')
@login_required
def search_users():
    search_term = request.args.get('term', '').strip()
    
    if len(search_term) < 2:
        return jsonify({'users': []})
    
    users = User.query.filter(
        User.username.ilike(f'%{search_term}%')
    ).filter(User.id != current_user.id).all()
    
    return jsonify({
        'users': [{
            'username': user.username
        } for user in users]
    })

@app.route('/api/share-data', methods=['POST'])
@login_required
def share_data():
    try:
        data = request.get_json()
        
        if not all(k in data for k in ['dataType', 'shareWith']):
            return jsonify({'success': False, 'message': 'Missing required fields'}), 400
        
        shared_with = User.query.filter_by(username=data['shareWith']).first()
        if not shared_with:
            return jsonify({'success': False, 'message': 'User not found'}), 404
        
        shared_expense = SharedExpense(
            shared_by_id=current_user.id,
            shared_with_id=shared_with.id,
            data_type=data['dataType'],
            categories=json.dumps(data.get('categories', [])) if data['dataType'] == 'summary' else None,
            start_date=datetime.strptime(data['startDate'], '%Y-%m-%d') if data.get('startDate') else None,
            end_date=datetime.strptime(data['endDate'], '%Y-%m-%d') if data.get('endDate') else None
        )
        
        db.session.add(shared_expense)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Data shared successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/shared-expenses')
@login_required
def get_shared_expenses():
    # Get expenses shared with current user
    shared_records = SharedExpense.query.filter_by(shared_with_id=current_user.id).all()
    
    result = []
    for record in shared_records:
        # Get the original expenses based on sharing criteria
        query = Expense.query.filter_by(user_id=record.shared_by_id)
        
        # Apply date filters if specified
        if record.start_date:
            query = query.filter(Expense.date >= record.start_date)
        if record.end_date:
            query = query.filter(Expense.date <= record.end_date)
            
        # Apply category filter if summary type
        if record.data_type == 'summary' and record.categories:
            categories = json.loads(record.categories)
            query = query.filter(Expense.category.in_(categories))
            
        expenses = query.all()
        
        # Format the data
        shared_data = {
            'shared_by': record.shared_by.username,
            'shared_at': record.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'data_type': record.data_type,
            'expenses': [{
                'date': exp.date.strftime('%Y-%m-%d'),
                'category': exp.category,
                'subCategory': exp.sub_category,
                'amount': exp.amount,
                'currency': exp.currency
            } for exp in expenses]
        }
        result.append(shared_data)
    
    return jsonify(result)

@app.route('/api/my-shared-expenses')
@login_required
def get_my_shared_expenses():
    # Get expenses shared by current user
    shared_records = SharedExpense.query.filter_by(shared_by_id=current_user.id).all()
    
    result = []
    for record in shared_records:
        result.append({
            'shared_with': record.shared_with.username,
            'shared_at': record.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'data_type': record.data_type,
            'categories': json.loads(record.categories) if record.categories else None,
            'start_date': record.start_date.strftime('%Y-%m-%d') if record.start_date else None,
            'end_date': record.end_date.strftime('%Y-%m-%d') if record.end_date else None
        })
    
    return jsonify(result)

@app.route('/debug/users')
@login_required
def debug_users():
    users = User.query.all()
    return jsonify({
        'users': [{
            'id': user.id,
            'username': user.username
        } for user in users]
    })

if __name__ == '__main__':
    app.run(debug=True)