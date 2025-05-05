# seed.py
from app import app
from models import db, User, Expense
from datetime import datetime, timedelta
import random

categories = {
    "Housing": ["rent", "mortgage"],
    "Food": ["grocery", "restaurants"],
    "Shopping": ["clothes", "electronics"],
    "Education": ["tuition", "printing"],
    "Others": ["gifts", "transport", "maintenance"]
}
currencies = ["AUD", "GBP", "USD", "CAD", "EUR"]

def seed():
    with app.app_context():
        db.drop_all()
        db.create_all()

        # Create a user
        user = User(username="demo_user", password_hash="hashedpassword")
        db.session.add(user)
        db.session.commit()

        # Generate fake expenses
        for _ in range(100):
            category = random.choice(list(categories.keys()))
            sub_category = random.choice(categories[category])
            amount = round(random.uniform(10, 500), 2)
            currency = random.choice(currencies)
            days_ago = random.randint(0, 180)
            date = datetime.utcnow() - timedelta(days=days_ago)

            expense = Expense(
                date=date,
                category=category,
                sub_category=sub_category,
                amount=amount,
                currency=currency,
                user_id=user.id
            )
            db.session.add(expense)

        db.session.commit()
        print("✅ Database seeded with fake data.")

if __name__ == "__main__":
    seed()
