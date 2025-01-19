Single-database configuration for Flask.


Wallet Web Application

Overview

The Wallet Web Application is a Flask-based web application developed in Python. This project manages financial data with five primary tables:

User: Represents individual users of the application.

Account: Stores account details, including user associations and financial balances.

Transaction: Records transactions linked to accounts with category and subcategory details.

Category: Manages high-level classifications for transactions.

Subcategory: Represents more granular classifications within a category.

The application supports CRUD operations and integrates SQLAlchemy for database interactions.


Features

User Management: Manage users and their financial accounts.

Account Tracking: Keep track of account balances, budgets, and transactions.

Transactions: Categorize income and expenses with associated categories and subcategories.

Budget Management: Monitor account expenses and check for budget exceedances.

Database Relationships: Comprehensive relational mapping with cascading delete behavior.


Technologies Used

Programming Language: Python 3

Web Framework: Flask

Database: SQLAlchemy (ORM)

Date Handling: datetime and date modules


Project Structure

Models

1. Account

Table Name: accounts

Primary Key: account_id

Fields: user_id, account_name, account_type, balance, budget, created_at

Relationships: Transactions linked to the account

2. Category

Table Name: categories

Primary Key: id

Fields: name

Relationships: Subcategories linked to the category

3. Subcategory

Table Name: subcategories

Primary Key: id

Fields: name, category_id

4. Transaction

Table Name: transactions

Primary Key: transaction_id

Fields: account_id, transaction_type, amount, created_at, description, category_id, subcategory_id

Relationships: Linked to categories, subcategories, and accounts

5. User

Represents users in the system (not fully detailed in the provided code).

Key Functionalities

Account Management:

Add, update, and delete accounts.

Calculate total expenses and check if budgets are exceeded.

Category and Subcategory Management:

Create and manage categories and subcategories.

Link categories and subcategories to transactions.

Transaction Management:

Record income and expense transactions.

Associate transactions with categories, subcategories, and accounts.


Installation and Setup

Clone the repository:git clone <repository-url>
cd wallet-web-application
Create a virtual environment:
python3 -m venv venv
source venv/bin/activate

Install dependencies:
pip install -r requirements.txt

Set up the database:
flask db init
flask db migrate
flask db upgrade

Run the application:
flask run

Access the application at http://127.0.0.1:5000/

Contact

For questions or support, please reach out to the project maintainer or open an issue on GitHub.

Author
This project was developed by Bayizere Marius 