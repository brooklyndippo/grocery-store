from ast import Store
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, SubmitField, FloatField, PasswordField, ValidationError
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, URL
from grocery_app.models import GroceryStore, ItemCategory, User
from grocery_app import bcrypt

class GroceryStoreForm(FlaskForm):
    """Form for adding/updating a GroceryStore."""
    title = StringField(label='Store Name')
    address = StringField(label='Address')
    #submit = SubmitField(label='Create Store')

def store_query():
    return GroceryStore.query

def get_choices():
    return ItemCategory.choices()

class GroceryItemForm(FlaskForm):
    """Form for adding/updating a GroceryItem."""
    name = StringField(label='Item Name')
    price = FloatField(label='Price')
    category = SelectField(label='Category', choices=get_choices)
    photo_url = StringField(label='Image')
    store = QuerySelectField(label='Store' , query_factory=store_query)
    #submit = SubmitField(label='Create Item')


class SignUpForm(FlaskForm):
    username = StringField('User Name',
        validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    username = StringField('User Name',
        validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if not user:
            raise ValidationError('No user with that username. Please try again.')

    def validate_password(self, password):
        user = User.query.filter_by(username=self.username.data).first()
        if user and not bcrypt.check_password_hash(
                user.password, password.data):
            raise ValidationError('Password doesn\'t match. Please try again.')