import os
from app import db
from datetime import datetime

print(os.path.abspath(__file__))


class Account(db.Model):
    __tablename__ = 'accounts'

    # account_id = db.Column(db.String(20), primary_key=True, nullable=False)
    account_id = db.Column(db.Integer, primary_key=True, nullable=False) 
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    account_name = db.Column(db.String(100), nullable=False)
    account_type = db.Column(db.String(50), nullable=False)
    balance = db.Column(db.Float, nullable=False)
    budget = db.Column(db.Float, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    transactions = db.relationship(
        'Transaction', backref='account', lazy=True, cascade="all, delete-orphan"
    )

    def __init__(self, user_id, account_name, account_type, balance, budget=None):
        self.user_id = user_id
        self.account_name = account_name
        self.account_type = account_type
        self.balance = balance
        self.budget = budget
        self.created_at = datetime.utcnow()
        print("Registered tables:", db.Model.metadata.tables.keys())

    def __repr__(self):
        return (
            f"Account('{self.account_id}', '{self.user_id}', '{self.account_name}', "
            f"'{self.account_type}', '{self.balance}', '{self.created_at}')"
        )

    def __str__(self):
        return f"Account: {self.account_name} ({self.account_type})"

    def get_total_expenses(self):
        """Calculate the total expenses for this account."""
        if not self.transactions:
            return 0.0
        return sum(
            transaction.amount for transaction in self.transactions if transaction.is_expense()
        )

    def is_budget_exceeded(self):
        """Check if the total expenses exceed the set budget."""
        if self.budget is not None:
            return self.get_total_expenses() > self.budget
        return False
