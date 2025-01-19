from app import db
from datetime import datetime
from app.routes import transaction
from app.models import Account, db
from app.views.forms import AccountForm
from flask import render_template, flash, redirect, url_for
from flask import Blueprint, request, render_template, redirect, url_for, flash

account_bp = Blueprint('account', __name__)
transaction_bp = Blueprint("transaction", __name__)


@account_bp.route('/add_account', methods=['GET', 'POST'])
def add_account():
    form = AccountForm()

    if form.validate_on_submit():
        new_account = Account(
            account_id=form.account_id.data,
            user_id=form.user_id.data,
            account_name=form.account_name.data,
            account_type=form.account_type.data,
            balance=form.balance.data,
            created_at=datetime.utcnow()
        )
        db.session.add(new_account)
        db.session.commit()
        flash('Account added successfully!', 'success')
        return redirect(url_for('account.display_accounts'))

    return render_template('add_account.html', form=form)

@account_bp.route('/accounts', methods=['GET'])
def display_accounts():
    accounts = Account.query.all()
    return render_template('display_accounts.html', accounts=accounts)

@account_bp.route('/update_account/<account_id>', methods=['GET', 'POST'])
def update_account(account_id):
    account = Account.query.get_or_404(account_id)
    form = AccountForm(obj=account)

    if request.method == 'POST' and form.validate_on_submit():
        account.user_id = form.user_id.data
        account.account_name = form.account_name.data
        account.account_type = form.account_type.data
        account.balance = form.balance.data
        db.session.commit()
        flash('Account updated successfully!', 'success')
        return redirect(url_for('account.display_accounts'))

    return render_template('update_account.html', form=form, account_id=account_id)


@account_bp.route('/delete_account/<account_id>', methods=['POST', 'DELETE'])
def delete_account(account_id):
    if request.method == 'DELETE':
        account = Account.query.get_or_404(account_id)
        for transaction in account.transactions:
            db.session.delete(transaction)
        db.session.delete(account)
        db.session.commit()
        flash('Account deleted successfully!', 'success')

    return redirect(url_for('account.display_accounts'))

@account_bp.route('/check_budget/<int:user_id>', methods=['GET'])
def check_budget(user_id):
    """Check if any account's expenses exceed the budget for a user."""
    user = User.query.get_or_404(user_id)
    budget_exceeded_accounts = []

    for account in user.accounts:
        if account.is_budget_exceeded():
            budget_exceeded_accounts.append({
                "account_name": account.account_name,
                "budget": account.budget,
                "total_expenses": account.get_total_expenses()
            })

    if budget_exceeded_accounts:
        flash("Warning: You have exceeded your budget in one or more accounts.", "danger")
        return render_template('budget_notification.html', exceeded_accounts=budget_exceeded_accounts)
    else:
        flash("Your budget is within limits for all accounts.", "success")
        return redirect(url_for('account.display_accounts'))



@account_bp.route('/set_budget/<int:account_id>', methods=['GET', 'POST'])
def set_budget(account_id):
    account = Account.query.get_or_404(account_id)

    if request.method == 'POST':
        user_id = request.form.get('user_id')
        account_id = request.form.get('account_id')
        budget_amount = request.form.get('budget')

        if user_id and account_id and budget_amount:
            account.budget = float(budget_amount)
            db.session.commit()
            flash(f"Budget updated successfully for account ID {account_id}.", "success")
            return redirect(url_for('account.display_accounts'))

    return render_template('set_budget.html', account=account, account_id=account_id, user_id=account.user_id)
