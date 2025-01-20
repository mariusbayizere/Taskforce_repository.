
from app import bcrypt
from flask import session
from app import db, bcrypt
from app.models import User
from flask_bcrypt import Bcrypt
from flask_bcrypt import Bcrypt
from werkzeug.security import generate_password_hash
from app.views.forms import UserForm, UpdateUserForm, LoginForm
from flask import Blueprint, render_template, redirect, url_for, flash

user_bp = Blueprint("user", __name__)


@user_bp.route("/add_user", methods=["GET", "POST"])
def add_user():
    form = UserForm()
    if form.validate_on_submit():
        raw_password = form.password.data.strip()
        print(f"[DEBUG] Plain password: {raw_password}")
        
        # Create new user without hashing the password here
        new_user = User(
            first_name=form.first_name.data.strip(),
            last_name=form.last_name.data.strip(),
            email=form.email.data.strip(),
            password=raw_password,  # Pass the raw password
            User_Role=form.User_Role.data
        )
        db.session.add(new_user)
        db.session.commit()
        print("[DEBUG] User added to the database.")
        
        flash("User created successfully.", "success")
        return redirect(url_for("user.display_users"))
    else:
        print("[DEBUG] Registration form validation failed.")
    
    return render_template("add_user.html", form=form)


@user_bp.route("/update_user/<int:user_id>", methods=["GET", "POST"])
def update_user(user_id):
    user = User.query.get_or_404(user_id)  
    form = UpdateUserForm(obj=user) 
    if form.validate_on_submit():  
        user.User_Role = form.User_Role.data
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.email = form.email.data
        
        try:
            db.session.commit() 
            flash("User updated successfully!", "success")
            return redirect(url_for("user.display_users"))
        except Exception as e:
            db.session.rollback()  
            flash(f"An error occurred: {str(e)}", "danger")

    return render_template("update_user.html", form=form, user=user)



# Delete a user
@user_bp.route("/delete_user/<int:user_id>", methods=["POST"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash("User deleted successfully!", "success")
    return redirect(url_for("user.display_users"))


# Display all users
@user_bp.route("/users")
def display_users():
    users = User.query.all()
    return render_template("display_users.html", users=users)


from werkzeug.security import generate_password_hash, check_password_hash



# @user_bp.route("/login", methods=["GET", "POST"])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         # Check if the email exists in the database
#         user = User.query.filter_by(email=form.email.data).first()
#         if user and check_password_hash(user.password, form.password.data):
#             session['user_id'] = user.id 
#             session['user_role'] = user.User_Role
#             flash(f"Welcome back, {user.first_name}!", "success")
#             return redirect(url_for("user.dashboard"))
#         else:
#             flash("Invalid email or password.", "danger")
#     return render_template("login.html", form=form)





@user_bp.route("/login", methods=["GET", "POST"])
def login():
    print("[DEBUG] Login route accessed")
    form = LoginForm()
    if form.validate_on_submit():
        print(f"[DEBUG] Form submitted with data:\n  Email: {form.email.data}\n  Password: {form.password.data}")
        
        # Query user from the database
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            print(f"[DEBUG] User found in the database:\n  ID: {user.id}, Email: {user.email}, Role: {user.User_Role}")
            print(f"[DEBUG] Stored hashed password: {user.password}")
            
            # Check password
            password_check = bcrypt.check_password_hash(user.password, form.password.data)
            print(f"[DEBUG] Password check result: {password_check}")
            
            if password_check:
                session.permanent = True  # Mark session as permanent (enforces timeout)
                session["user_id"] = user.id
                flash("Login successful!", "success")
                
                # Redirect based on role
                if user.User_Role.lower() == "admin":
                    return redirect(url_for("user.display_users"))
                elif user.User_Role.lower() == "user":
                    return redirect(url_for("user.display_users"))
                else:
                    flash("User role is not recognized.", "danger")
            else:
                print("[DEBUG] Incorrect password provided")
                flash("Login Unsuccessful. Please check email and password", "danger")
        else:
            print("[DEBUG] User not found")
            flash("Login Unsuccessful. Please check email and password", "danger")
    return render_template("login.html", form=form)



@user_bp.route("/logout", methods=["GET"])
def logout():
    session.clear() 
    flash("You have been logged out.", "success")
    return redirect(url_for("user.login")) 



# @user_bp.route("/dashboard")
# def dashboard():
#     if 'user_id' not in session:
#         flash("Please log in to access the dashboard.", "danger")
#         return redirect(url_for("user.login"))
#     return render_template("dashboard.html")

# At the top of app/routes/users.py
from flask import render_template, flash, redirect, url_for, session
from app.models.account import Account
from app.models.transaction import Transaction
from app.models.user import User
from app import db

@user_bp.route("/dashboard")
def dashboard():
    try:
        # Get all accounts for the user (this can be public or demo data if no login is required)
        user_accounts = Account.query.all()  # You can fetch public accounts or allow demo data

        # Initialize totals and transactions list
        total_income = 0
        total_expense = 0
        transactions = []
        
        # Aggregate transactions from all accounts (assuming public access)
        for account in user_accounts:
            # Get transactions for this account, order by most recent, limit to 10
            account_transactions = Transaction.query.filter_by(
                account_id=account.account_id
            ).order_by(Transaction.created_at.desc()).limit(10).all()

            # Add transactions to the list and calculate totals
            for t in account_transactions:
                transactions.append(t)
                if t.is_income():
                    total_income += t.amount
                elif t.is_expense():
                    total_expense += t.amount
        
        # Sort all transactions by date (most recent first)
        transactions.sort(key=lambda x: x.created_at, reverse=True)
        
        # Keep only the 10 most recent transactions across all accounts
        transactions = transactions[:10]
        
        # Calculate balance
        balance = total_income - total_expense
        
        return render_template(
            "dashboard.html",
            transactions=transactions,
            total_income=total_income,
            total_expense=total_expense,
            balance=balance
        )
    
    except Exception as e:
        # Log the error and flash a user-friendly message
        print(f"Error in dashboard route: {str(e)}")
        flash("An error occurred while loading the dashboard.", "danger")
        return redirect(url_for("user.dashboard"))


from app.models import Account

# @user_bp.route("/dashboard")
# def dashboard():
#     if 'user_id' not in session:
#         flash("Please log in to access the dashboard.", "danger")
#         return redirect(url_for("user.login"))

#     # Retrieve account_id for the logged-in user
#     user_id = session['user_id']
#     account = Account.query.filter_by(user_id=user_id).first()

#     if account:
#         account_id = account.account_id
#     else:
#         account_id = None  # Handle case where no account is found

#     return render_template("dashboard.html", account_id=account_id)


# def get_account_ids():
#     account_ids = [account.account_id for account in Account.query.all()]
#     return account_ids



# @user_bp.route("/dashboard")
# def dashboard():
#     if 'user_id' not in session:
#         flash("Please log in to access the dashboard.", "danger")
#         return redirect(url_for("user.login"))
    
#     account_ids = get_account_ids()
    
#     return render_template("dashboard.html", account_ids=account_ids)


# @user_bp.route("/dashboard")
# def dashboard():
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


@user_bp.route("/home")
def home():
    return render_template("HomePage.html")

@user_bp.route("/about")
def about():
    return render_template("HomePage.html")

@user_bp.route("/contact")
def contact():
    return render_template("HomePage.html")
