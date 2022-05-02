from ast import Store
from tkinter.tix import Select
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, SubmitField, FloatField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, URL

class GroceryStoreForm(FlaskForm):
    """Form for adding/updating a GroceryStore."""
    title = StringField(label='Store Name', validators=[DataRequired])
    address = StringField(label='Address', validators=[DataRequired])
    submit_button = SubmitField(label='Submit')

def store_query():
    return Store.query

class GroceryItemForm(FlaskForm):
    """Form for adding/updating a GroceryItem."""
    name = StringField(label='Item Name', validators=[DataRequired])
    price = FloatField(label='Price', validators=[DataRequired])
    category = SelectField(label='Category', choices=['Produce', 'Bread', 'Dairy', 'Meat/Seafood', 'Frozen', 'Snack', 'Other'])
    photo_url = StringField(label='Image', validators=[DataRequired])
    store = QuerySelectField(label='Store', query_factory=store_query)
    submit_button = SubmitField(label='Submit')
