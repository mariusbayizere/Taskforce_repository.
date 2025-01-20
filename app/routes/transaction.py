from app.models.category import *
from app.models.account import Account
from flask import Blueprint, flash, redirect, render_template, request, url_for
from app.models import Transaction, db
from app import db
from app.views.forms import TransactionForm  # Assuming you have a form for Transaction

transaction_bp = Blueprint("transaction", __name__)



# @transaction_bp.route("/add_transaction", methods=["GET", "POST"])
# def add_transaction():
#     transaction_form = TransactionForm()

#     if transaction_form.validate_on_submit():  # Validate form data
#         # Ensure account ID exists in the database
#         account_id = transaction_form.account_id.data
#         account = Account.query.filter_by(account_id=account_id).first()
#         if not account:
#             flash("Invalid account ID.", "danger")
#             return render_template("add_transaction.html", form=transaction_form)

#         # Extract transaction details
#         transaction_type = transaction_form.transaction_type.data
#         amount = transaction_form.amount.data
#         description = transaction_form.description.data

#         # Debugging: Print account and budget details
#         print(f"Account: {account.account_name}, Budget: {account.budget}, Type: {transaction_type}, Amount: {amount}")

#         # Check for budget exceedance if the transaction is an expense
#         if transaction_type.lower() == "expense":
#             if account.budget is not None and amount > account.budget:
#                 flash(f"Expense of {amount} exceeds the budget of {account.budget}!", "danger")
#                 return render_template("add_transaction.html", form=transaction_form)

#         # Create and save the transaction
#         new_transaction = Transaction(
#             account_id=account_id,
#             transaction_type=transaction_type,
#             amount=amount,
#             description=description,
#             category_id=category_id,
#             subcategory_id=subcategory_id,
#         )
#         db.session.add(new_transaction)
#         db.session.commit()

#         flash("Transaction added successfully!", "success")
#         return redirect(url_for("transaction.display_transactions"))

#     # Render the form if GET request or validation fails
#     return render_template("add_transaction.html", form=transaction_form)

# -------------------



@transaction_bp.route("/add_transaction", methods=["GET", "POST"])
def add_transaction():
    transaction_form = TransactionForm()

    # Populate category_id and subcategory_id choices
    transaction_form.category_id.choices = [(cat.id, cat.name) for cat in Category.query.all()]
    transaction_form.subcategory_id.choices = [(sub.id, sub.name) for sub in Subcategory.query.all()]

    if transaction_form.validate_on_submit():  # Validate form data
        # Ensure account ID exists in the database
        account_id = transaction_form.account_id.data
        account = Account.query.filter_by(account_id=account_id).first()
        if not account:
            flash("Invalid account ID.", "danger")
            return render_template("add_transaction.html", form=transaction_form)

        # Extract transaction details
        transaction_type = transaction_form.transaction_type.data
        amount = transaction_form.amount.data
        description = transaction_form.description.data
        category_id = transaction_form.category_id.data  # Retrieve selected category ID
        subcategory_id = transaction_form.subcategory_id.data  # Retrieve selected subcategory ID

        # Check for budget exceedance if the transaction is an expense
        if transaction_type.lower() == "expense":
            if account.budget is not None and amount > account.budget:
                flash(f"Expense of {amount} exceeds the budget of {account.budget}!", "danger")
                return render_template("add_transaction.html", form=transaction_form)

        # Create and save the transaction
        # new_transaction = Transaction(
        #     account_id=account_id,
        #     transaction_type=transaction_type,
        #     amount=amount,
        #     description=description,
        #     category_id=category_id,
        #     subcategory_id=subcategory_id,
        # )
        new_transaction = Transaction(
            account_id=account_id,
            transaction_type=transaction_type,
            amount=amount,
            description=description,
            category_id=category_id,
            subcategory_id=subcategory_id,
        )


        db.session.add(new_transaction)
        db.session.commit()

        flash("Transaction added successfully!", "success")
        return redirect(url_for("transaction.display_transactions"))

    # Render the form if GET request or validation fails
    return render_template("add_transaction.html", form=transaction_form)




# @transaction_bp.route("/update_transaction/<int:transaction_id>", methods=["GET", "POST"])
# def update_transaction(transaction_id):
#     transaction = Transaction.query.get_or_404(transaction_id)
#     transaction_form = TransactionForm(obj=transaction)

#     if request.method == "POST" and transaction_form.validate_on_submit():
#         transaction.account_id = transaction_form.account_id.data
#         transaction.transaction_type = transaction_form.transaction_type.data
#         transaction.amount = transaction_form.amount.data
#         transaction.created_at = transaction_form.created_at.data
#         transaction.description = transaction_form.description.data

#         db.session.commit()

#         flash("Transaction updated successfully!", "success")
#         return redirect(url_for("transaction.display_transactions"))

#     # Pass `transaction_form` to the template as `form`
#     return render_template(
#         "update_transaction.html",
#         form=transaction_form,  # Alias transaction_form as form
#         transaction_id=transaction_id,
#     )


from flask import current_app

@transaction_bp.route("/update_transaction/<int:transaction_id>", methods=["GET", "POST"])
def update_transaction(transaction_id):
    transaction = Transaction.query.get_or_404(transaction_id)
    transaction_form = TransactionForm(obj=transaction)

    # Dynamically set the choices for category and subcategory fields
    transaction_form.category_id.choices = [(c.id, c.name) for c in Category.query.all()]
    transaction_form.subcategory_id.choices = [(s.id, s.name) for s in Subcategory.query.all()]

    if request.method == "POST" and transaction_form.validate_on_submit():
        transaction.account_id = transaction_form.account_id.data
        transaction.transaction_type = transaction_form.transaction_type.data
        transaction.amount = transaction_form.amount.data
        transaction.created_at = transaction_form.created_at.data
        transaction.description = transaction_form.description.data
        transaction.category_id = transaction_form.category_id.data
        transaction.subcategory_id = transaction_form.subcategory_id.data

        db.session.commit()

        flash("Transaction updated successfully!", "success")
        return redirect(url_for("transaction.display_transactions"))

    return render_template(
        "update_transaction.html",
        form=transaction_form,
        transaction_id=transaction_id,
    )




@transaction_bp.route("/delete_transaction/<int:transaction_id>", methods=["POST"])
# @login_required
def delete_transaction(transaction_id):
    transaction = Transaction.query.get_or_404(transaction_id)
    db.session.delete(transaction)
    db.session.commit()
    flash("Transaction deleted successfully!", "success")
    return redirect(url_for("transaction.display_transactions"))


# @transaction_bp.route("/transactions", methods=["GET"])
# def display_transactions():
#     transactions = Transaction.query.all()
#     return render_template("display_transactions.html", transactions=transactions)

# @transaction_bp.route("/account/<int:account_id>/transactions", methods=["GET"])
# def view_account_transactions(account_id):
#     # Fetch all transactions for the account
#     transactions = Transaction.query.filter_by(account_id=account_id).order_by(Transaction.created_at).all()

#     if not transactions:
#         flash(f"No transactions found for Account ID {account_id}", "warning")
#         return redirect(url_for("transaction.add_transaction"))

#     # Calculate totals
#     total_income = sum(t.amount for t in transactions if t.is_income())
#     total_expense = sum(t.amount for t in transactions if t.is_expense())
#     balance = total_income - total_expense

#     return render_template(
#         "account_transactions.html",
#         transactions=transactions,
#         total_income=total_income,
#         total_expense=total_expense,
#         balance=balance,
#     )



# In your Flask blueprint
@transaction_bp.route("/account/<int:account_id>/transactions", methods=["GET"])
def view_account_transactions(account_id):

    account = Account.query.get(account_id)  # Check if the account exists
    if not account:
        flash(f"No account found with ID {account_id}. Please create an account.", "danger")
        return redirect(url_for('account.create_account'))  # Redirect to account creation page

    transactions = Transaction.query.filter_by(account_id=account_id).order_by(Transaction.created_at).all()

    if not transactions:
        flash(f"No transactions found for Account ID {account_id}", "warning")
        return redirect(url_for("transaction.add_transaction"))

    # Calculate totals
    total_income = sum(t.amount for t in transactions if t.is_income())
    total_expense = sum(t.amount for t in transactions if t.is_expense())
    balance = total_income - total_expense

    return render_template(
        "account_transactions.html",
        transactions=transactions,
        total_income=total_income,
        total_expense=total_expense,
        balance=balance,
    )






# @transaction_bp.route("/account/<int:account_id>/transactions", methods=["GET"])
# def view_account_transactions(account_id):
#     if 'user_id' not in session:
#         flash("Please log in to access the dashboard.", "danger")
#         return redirect(url_for("user.login"))
    
#     # Fetch all accounts for the user
#     accounts = Account.query.filter_by(user_id=session['user_id']).all()
    
#     # Fetch all transactions for all accounts
#     transactions = []
#     for account in accounts:
#         account_transactions = Transaction.query.filter_by(account_id=account.account_id).order_by(Transaction.created_at).all()
#         transactions.extend(account_transactions)
    
#     # Calculate totals
#     total_income = sum(t.amount for t in transactions if t.is_income())
#     total_expense = sum(t.amount for t in transactions if t.is_expense())
#     balance = total_income - total_expense
    
#     return render_template(
#         "dashboard.html",
#         transactions=transactions,
#         total_income=total_income,
#         total_expense=total_expense,
#         balance=balance,
#     )


from datetime import datetime

# @transaction_bp.route('/generate_report', methods=['GET', 'POST'])
# def generate_report():
#     if request.method == 'POST':
#         # Get the start and end dates from the form
#         start_date_str = request.form.get('start_date')
#         end_date_str = request.form.get('end_date')

#         if not start_date_str or not end_date_str:
#             flash("Both start and end dates are required.", "danger")
#             return render_template('generate_report.html')

#         try:
#             # Convert strings to date objects
#             start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
#             end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

#             # Query transactions within the date range
#             transactions = Transaction.query.filter(
#                 Transaction.created_at.between(start_date, end_date)
#             ).all()

#             if not transactions:
#                 flash("No transactions found for the selected date range.", "info")
#                 return render_template('generate_report.html')

#             # Calculate total income, total expense, and balance
#             total_income = sum(t.amount for t in transactions if t.is_income())
#             total_expense = sum(t.amount for t in transactions if t.is_expense())
#             balance = total_income - total_expense

#             return render_template(
#                 'report.html',
#                 transactions=transactions,
#                 total_income=total_income,
#                 total_expense=total_expense,
#                 balance=balance,
#                 start_date=start_date,
#                 end_date=end_date
#             )
#         except ValueError:
#             flash("Invalid date format. Please use YYYY-MM-DD.", "danger")
#             return render_template('generate_report.html')

#     # Default GET request
#     return render_template('generate_report.html')

from datetime import timedelta

# @transaction_bp.route('/generate_report', methods=['GET', 'POST'])
# def generate_report():
#     if request.method == 'POST':
#         # Get the option selected by the user
#         report_option = request.form.get('report_option')

#         # Calculate the date range based on the option chosen
#         if report_option == 'today':
#             start_date = datetime.today().date()
#             end_date = start_date
#         elif report_option == 'week':
#             start_date = datetime.today() - timedelta(days=datetime.today().weekday())  # Start of the week
#             end_date = start_date + timedelta(days=6)  # End of the week
#         elif report_option == 'month':
#             today = datetime.today()
#             start_date = today.replace(day=1)  # Start of the month
#             end_date = today.replace(day=28) + timedelta(days=4)  # End of the month (approximated)
#             end_date = end_date - timedelta(days=end_date.day)  # Correct the end date to the last day of the month
#         else:
#             start_date_str = request.form.get('start_date')
#             end_date_str = request.form.get('end_date')

#             if not start_date_str or not end_date_str:
#                 flash("Both start and end dates are required.", "danger")
#                 return render_template('generate_report.html')

#             try:
#                 # Convert strings to date objects
#                 start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
#                 end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
#             except ValueError:
#                 flash("Invalid date format. Please use YYYY-MM-DD.", "danger")
#                 return render_template('generate_report.html')

#         # Query transactions within the calculated date range
#         transactions = Transaction.query.filter(
#             Transaction.created_at.between(start_date, end_date)
#         ).all()

#         if not transactions:
#             flash("No transactions found for the selected date range.", "info")
#             return render_template('generate_report.html')

#         # Calculate total income, total expense, and balance
#         total_income = sum(t.amount for t in transactions if t.is_income())
#         total_expense = sum(t.amount for t in transactions if t.is_expense())
#         balance = total_income - total_expense

#         return render_template(
#             'report.html',
#             transactions=transactions,
#             total_income=total_income,
#             total_expense=total_expense,
#             balance=balance,
#             start_date=start_date,
#             end_date=end_date
#         )

#     # Default GET request
#     return render_template('generate_report.html')

@transaction_bp.route('/generate_report', methods=['GET', 'POST'])
def generate_report():
    if request.method == 'POST':
        # Get the option selected by the user
        report_option = request.form.get('report_option')

        # Calculate the date range based on the option chosen
        if report_option == 'today':
            start_date = datetime.today().replace(microsecond=0)
            end_date = start_date
        elif report_option == 'week':
            start_date = (datetime.today() - timedelta(days=datetime.today().weekday())).replace(microsecond=0)
            end_date = (start_date + timedelta(days=6)).replace(microsecond=0)
        elif report_option == 'month':
            today = datetime.today().replace(microsecond=0)
            start_date = today.replace(day=1)
            end_date = today.replace(day=28) + timedelta(days=4)
            end_date = end_date - timedelta(days=end_date.day)
            end_date = end_date.replace(microsecond=0)
        else:
            start_date_str = request.form.get('start_date')
            end_date_str = request.form.get('end_date')

            if not start_date_str or not end_date_str:
                flash("Both start and end dates are required.", "danger")
                return render_template('generate_report.html')

            try:
                # Convert strings to date objects
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').replace(microsecond=0)
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').replace(microsecond=0)
            except ValueError:
                flash("Invalid date format. Please use YYYY-MM-DD.", "danger")
                return render_template('generate_report.html')

        # Query transactions within the calculated date range
        transactions = Transaction.query.filter(
            Transaction.created_at.between(start_date, end_date)
        ).all()

        if not transactions:
            flash("No transactions found for the selected date range.", "info")
            return render_template('generate_report.html')

        # Calculate total income, total expense, and balance
        total_income = sum(t.amount for t in transactions if t.is_income())
        total_expense = sum(t.amount for t in transactions if t.is_expense())
        balance = total_income - total_expense

        return render_template(
            'report.html',
            transactions=transactions,
            total_income=total_income,
            total_expense=total_expense,
            balance=balance,
            start_date=start_date.strftime('%Y-%m-%d %H:%M'),
            end_date=end_date.strftime('%Y-%m-%d %H:%M')
        )

    # Default GET request
    return render_template('generate_report.html')


@transaction_bp.route('/set_budget', methods=['GET', 'POST'])
def set_budget():
    if request.method == 'POST':
        user_id = request.form.get('user_id', type=int)
        account_id = request.form.get('account_id')
        budget = request.form.get('amount', type=float)
        
        # Validate user and account existence
        account = Account.query.filter_by(account_id=account_id, user_id=user_id).first()
        if not account:
            flash('Invalid User ID or Account ID', 'danger')
            return redirect(url_for('transaction.set_budget'))

        if budget <= 0:
            flash('Budget must be greater than 0', 'danger')
            return redirect(url_for('transaction.set_budget'))
        
        # Set the budget
        account.budget = budget
        db.session.commit()
        
        flash(f'Budget of {budget} set for Account {account.account_name}', 'success')
        return redirect(url_for('transaction.display_transactions'))

    return render_template('set_budget.html')


@transaction_bp.route('/check_transaction', methods=['POST'])
def check_transaction():
    account_id = request.form.get('account_id')
    transaction_type = request.form.get('transaction_type')
    amount = request.form.get('amount', type=float)
    description = request.form.get('description', '')

    account = Account.query.filter_by(account_id=account_id).first()
    if not account:
        flash('Account not found', 'danger')
        return redirect(url_for('transaction.display_transactions'))

    # Check for budget exceedance
    if transaction_type.lower() == 'expense':
        if account.budget is not None and amount > account.budget:
            flash(f'Expense of {amount} exceeds the budget of {account.budget}!', 'danger')
            return redirect(url_for('transaction.display_transactions'))

    # Add the transaction
    transaction = Transaction(
        account_id=account_id,
        transaction_type=transaction_type,
        amount=amount,
        description=description,
    )
    db.session.add(transaction)
    db.session.commit()

    flash('Transaction added successfully!', 'success')
    return redirect(url_for('transaction.display_transactions'))
