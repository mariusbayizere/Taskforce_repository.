from datetime import datetime, timedelta
from flask import Flask, session, redirect, url_for, flash, request
from app.routes.errors import errors_bp
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

# Extensions
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()

def init_app(app):
    """Initialize Flask extensions and databases"""
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    return app

def create_app():
    app = Flask(__name__)
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:auca%402023@localhost/wallet_app'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://root:bCObtI42AoEx5wE1Rux3KOhJ0zq3wMch@dpg-cu79rdrtq21c739l0ehg-a/wallet_app_0qy4'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = False
    app.secret_key = 'c89e61772573f1b017aa1ce7d45b839a87e41f61297455d6'
    app.permanent_session_lifetime = timedelta(minutes=2) 
    init_app(app)


    from app.routes.users import user_bp
    from app.routes.accounts import account_bp
    from app.routes.transaction import transaction_bp
    from app.routes.category import categoriesbp
    from app.routes.category import subcategoriesbp
    from app.routes.get_transaction_summary import visualization_bp

    app.register_blueprint(errors_bp)
    app.register_blueprint(user_bp, url_prefix='/add_user')
    app.register_blueprint(subcategoriesbp, url_prefix='/subcategories')
    app.register_blueprint(categoriesbp, url_prefix='/categories')
    app.register_blueprint(account_bp, url_prefix='/add_account')
    app.register_blueprint(transaction_bp, url_prefix='/add_transaction')
    app.register_blueprint(visualization_bp, url_prefix='/api/transactions/summary')

    @app.route('/')
    def index():
        return redirect(url_for('user.login'))

    @app.before_request
    def check_session_timeout():
        session_lifetime = timedelta(minutes=2)

        if 'last_activity' not in session:
            session['last_activity'] = datetime.now()
            print(f"Session start time (set on login): {session['last_activity']}")

        session_start = session['last_activity']
        print(f"Session start time: {session_start}")

        if session_start.tzinfo is not None:
            session_start = session_start.replace(tzinfo=None)
            print(f"Session start time (naive): {session_start}")

        current_time = datetime.now()
        if current_time.tzinfo is not None:
            current_time = current_time.replace(tzinfo=None)
        print(f"Current time (naive): {current_time}")

        time_diff = current_time - session_start
        print(f"Time difference: {time_diff}")

        if time_diff > session_lifetime:
            print("Session timeout exceeded. Clearing session...")
            session.clear()
            flash("Session expired due to inactivity", "danger")
            return redirect(url_for('user.login'))  
        if request.endpoint not in ['user.login', 'user.logout']:
            session['last_activity'] = datetime.now()
            print(f"Last activity time updated: {session['last_activity']}")


    return app
