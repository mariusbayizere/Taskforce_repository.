# from app import db
# from sqlalchemy.orm import relationship
# from datetime import date
# from .account import Account
# import os


# print(os.path.abspath(__file__))

# class Transaction(db.Model):
#     __tablename__ = 'transactions'

#     transaction_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
#     account_id = db.Column(db.String(20), db.ForeignKey('accounts.account_id'), nullable=False)
#     transaction_type = db.Column(db.String(100), nullable=False)
#     amount = db.Column(db.Float, nullable=False)
#     # created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#     created_at = db.Column(db.Date, nullable=False, default=date.today)
#     description = db.Column(db.String(100), nullable=True)
    

#     print("Test two Transaction Table ....")

#     def __init__(self, account_id, transaction_type, amount, description=None):
#         self.account_id = account_id
#         self.transaction_type = transaction_type
#         self.amount = amount
#         self.description = description
#         # self.created_at = created_at if created_at else date.today()

#         print("Registered tables:", db.Model.metadata.tables.keys())
   
#     def __repr__(self):
#         """
#         Provide an unambiguous string representation of the Transaction object.
        
#         Returns:
#             str: A string representation of the transaction.
#         """
#         return (f"Transaction('{self.transaction_id}', '{self.account_id}', "
#                 f"'{self.transaction_type}', '{self.amount}', '{self.created_at}', "
#                 f"'{self.description}')")

#     def is_income(self):
#         return self.transaction_type.lower() == "income"

#     def is_expense(self):
#         return self.transaction_type.lower() == "expense"
    
#     def __str__(self):
#         """
#         Provide a readable string representation of the Transaction object.
        
#         Returns:
#             str: A string describing the transaction type and amount.
#         """
#         return f"Transaction: {self.transaction_type} ({self.amount})"


from app import db
from sqlalchemy.orm import relationship
from datetime import date
from .account import Account
import os


print(os.path.abspath(__file__))

class Transaction(db.Model):
    __tablename__ = 'transactions'

    transaction_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    account_id = db.Column(db.String(20), db.ForeignKey('accounts.account_id'), nullable=False)
    transaction_type = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.Date, nullable=False, default=date.today)
    description = db.Column(db.String(100), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
    subcategory_id = db.Column(db.Integer, db.ForeignKey('subcategories.id'), nullable=True)

    category = relationship('Category', backref='transactions', lazy=True)
    subcategory = relationship('Subcategory', backref='transactions', lazy=True)

    def __init__(self, account_id, transaction_type, amount, description=None, category_id=None, subcategory_id=None):
        self.account_id = account_id
        self.transaction_type = transaction_type
        self.amount = amount
        self.description = description
        self.category_id = category_id
        self.subcategory_id = subcategory_id



        print("Registered tables:", db.Model.metadata.tables.keys())
   
    def __repr__(self):
        """
        Provide an unambiguous string representation of the Transaction object.
        
        Returns:
            str: A string representation of the transaction.
        """
        return (f"Transaction('{self.transaction_id}', '{self.account_id}', "
                f"'{self.transaction_type}', '{self.amount}', '{self.created_at}', "
                f"'{self.description}')")

    def is_income(self):
        return self.transaction_type.lower() == "income"

    def is_expense(self):
        return self.transaction_type.lower() == "expense"
    
    def __str__(self):
        """
        Provide a readable string representation of the Transaction object.
        
        Returns:
            str: A string describing the transaction type and amount.
        """
        return f"Transaction: {self.transaction_type} ({self.amount})"

