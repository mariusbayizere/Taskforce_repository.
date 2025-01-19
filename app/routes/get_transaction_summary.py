from flask import Blueprint, jsonify
from app import db
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from app.models.transaction import Transaction

visualization_bp = Blueprint('visualization', __name__)
@visualization_bp.route("/transactions_summary")
def transactions_summary():
    # Fetch transactions from the database
    transactions = Transaction.query.all()

    # Convert transactions to a pandas DataFrame
    data = [{
        "transaction_type": txn.transaction_type,
        "amount": txn.amount,
        "category": txn.category.name if txn.category else "Uncategorized",
        "subcategory": txn.subcategory.name if txn.subcategory else "None",
        "date": txn.timestamp
    } for txn in transactions]

    df = pd.DataFrame(data)

    # Summarize by transaction type
    type_summary = df.groupby("transaction_type")["amount"].sum().to_dict()

    # Summarize by category
    category_summary = df.groupby("category")["amount"].sum().to_dict()

    # Render the summary template with data
    return render_template(
        "transactions_summary.html",
        type_summary=type_summary,
        category_summary=category_summary,
    )