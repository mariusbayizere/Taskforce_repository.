import os
import re
from datetime import date   
from app.models import User 
from datetime import datetime
from flask_wtf import FlaskForm 
from wtforms.fields import DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from wtforms.validators import DataRequired, Length, Email, EqualTo
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import DataRequired, Length,  Email, NumberRange
from wtforms import Form, StringField, PasswordField, BooleanField, EmailField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms import SelectField,StringField, PasswordField, SubmitField, EmailField
from wtforms import IntegerField, StringField, HiddenField,FloatField, SelectField, DateTimeField, SubmitField, DecimalField

class TransactionForm(FlaskForm):
    account_id = IntegerField("Account ID", validators=[DataRequired()])
    transaction_type = SelectField(
        "Transaction Type",
        choices=[("Expense", "Expense"), ("Income", "Income")],
        validators=[DataRequired()],
    )
    amount = FloatField("Amount", validators=[DataRequired()])
    # created_at = DateField("Created At", format='%Y-%m-%d', default=None)
    created_at = DateField('Created At', format='%Y-%m-%d', default=None, validators=[DataRequired()])
    description = StringField("Description", validators=[DataRequired(), Length(max=100)])
    category_id = SelectField("Category", coerce=int, validators=[DataRequired()])
    subcategory_id = SelectField("Subcategory", coerce=int, validators=[DataRequired()])
    submit = SubmitField("Submit")

    # Custom validation for transaction_type
    def validate_transaction_type(form, field):
        if field.data not in ["Expense", "Income"]:
            raise ValidationError("Transaction Type must be either 'Expense' or 'Income'.")

    # Custom validation for created_at
    def validate_created_at(form, field):
        if field.data < date.today():
            raise ValidationError("You can not make Transaction on the Past!! please Change it to the future.")

    # Custom validation for description
    def validate_description(form, field):
        if len(field.data.split()) < 10:
            raise ValidationError("Description must contain at least 10 words.")


class AccountForm(FlaskForm):
    # account_id = LongField('Account ID', validators=[DataRequired()])
    account_id = IntegerField('Account ID', validators=[DataRequired()])
    user_id = IntegerField('User ID', validators=[DataRequired()])
    account_name = StringField('Account Name', validators=[DataRequired(), Length(max=100)])
    account_type = SelectField(
        'Account Type',
        choices=[('Bank Account', 'Bank account'),  ('Mobile Money Account', 'Mobile money account'), ('Cash Account', 'cash account')],
        validators=[DataRequired()]
    )
    balance = FloatField('Balance', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_account_id(form, field):
        if not isinstance(field.data, int) or field.data < -2**63 or field.data >= 2**63:
            raise ValidationError("Value must fit in a signed 64-bit long integer range (-2^63 to 2^63-1).")

class UserForm(FlaskForm):

    User_Role = SelectField(
        'User Role',
        choices=[
            ('User', 'User'),
            ('Admin', 'Admin')
        ],
        validators=[DataRequired(message="User Role is required.")]
    )



    first_name = StringField(
        'First Name',
        validators=[
            DataRequired(message="First Name is required."),
            Length(max=100, message="First Name must not exceed 100 characters.")
        ]
    )
    last_name = StringField(
        'Last Name',
        validators=[
            DataRequired(message="Last Name is required."),
            Length(max=100, message="Last Name must not exceed 100 characters.")
        ]
    )
    email = EmailField(
        'Email',
        validators=[
            DataRequired(message="Email is required."),
            Email(message="Invalid email format."),
            Length(max=100, message="Email must not exceed 100 characters.")
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(message="Password is required."),
            Length(min=6, message="Password must be at least 6 characters long.")
        ]
    )
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired(message="Please confirm your password."),
            EqualTo('password', message="Passwords must match.")
        ]
    )
    submit = SubmitField('Submit')


    def validate_email(self, email):
        if not email.data:  # Check if email field is empty
            raise ValidationError("Email is required.")

        # Check if email contains spaces
        if " " in email.data:
            raise ValidationError("Email must not contain spaces.")

        # Check if email contains uppercase letters
        if any(char.isupper() for char in email.data):
            raise ValidationError("Email must be in lowercase.")

        # Check if email includes '@'
        if "@" not in email.data:
            raise ValidationError("Email must include '@'.")

        # Check if email ends with '@gmail.com'
        if not email.data.endswith("@gmail.com"):
            raise ValidationError("Email must end with '@gmail.com'.")

        # Check if email already exists in the database
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email already exists. Please choose a different email.")


    def validate_password(self, password):
        if len(password.data) < 6:
            raise ValidationError("Password must be at least 6 characters long.")

        # Check if password contains uppercase letters
        if not any(char.isupper() for char in password.data):
            raise ValidationError("Password must contain at least one uppercase letter.")

        # Check if password contains lowercase letters
        if not any(char.islower() for char in password.data):
            raise ValidationError("Password must contain at least one lowercase letter.")

        # Check if password contains digits
        if not any(char.isdigit() for char in password.data):
            raise ValidationError("Password must contain at least one digit.")

        # Check if password contains special characters
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password.data):
            raise ValidationError("Password must contain at least one special character.")
        
        if self.confirm_password.data != password.data:
            raise ValidationError("Passwords must match.")

        if len(self.confirm_password.data) < 6:
            raise ValidationError("Confirm Password must be at least 6 characters long.")

        if not any(char.isupper() for char in self.confirm_password.data):
            raise ValidationError("Confirm Password must contain at least one uppercase letter.")

        if not any(char.islower() for char in self.confirm_password.data):
            raise ValidationError("Confirm Password must contain at least one lowercase letter.")

        if not any(char.isdigit() for char in self.confirm_password.data):
            raise ValidationError("Confirm Password must contain at least one digit.")

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', self.confirm_password.data):
            raise ValidationError("Confirm Password must contain at least one special character.")


class UpdateUserForm(FlaskForm):
    User_Role = StringField('User_Role', validators=[DataRequired(), Length(max=50)])
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=100)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=100)])
    email = EmailField('Email', validators=[DataRequired(), Email(), Length(max=100)])
    password = PasswordField('Password',validators=[DataRequired(message="Password is required."), Length(min=6)])
    submit = SubmitField('Update')



class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Login')

class DeleteAccountForm(FlaskForm):
    account_id = HiddenField('Account ID', validators=[DataRequired()])



class CategoryForm(FlaskForm):
    name = StringField("Category Name", validators=[DataRequired(), Length(max=50)])
    submit = SubmitField("Save")

class SubcategoryForm(FlaskForm):
    name = StringField("Subcategory Name", validators=[DataRequired(), Length(max=50)])
    category_id = SelectField("Category", coerce=int, validators=[DataRequired()])
    submit = SubmitField("Save")

class BudgetForm(FlaskForm):
    budget = DecimalField('Budget Amount', validators=[DataRequired()])

print(os.path.abspath(__file__))