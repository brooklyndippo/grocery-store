from ast import Store
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, SubmitField, FloatField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, URL

class GroceryStoreForm(FlaskForm):
    """Form for adding/updating a GroceryStore."""
    title = StringField(label='Store Name')
    address = StringField(label='Address')
    submit = SubmitField(label='Create Store')

def store_query():
    return Store.query

class GroceryItemForm(FlaskForm):
    """Form for adding/updating a GroceryItem."""
    name = StringField(label='Item Name')
    price = FloatField(label='Price')
    category = SelectField(label='Category', choices=['Produce', 'Bread', 'Dairy', 'Meat/Seafood', 'Frozen', 'Snack', 'Other'])
    photo_url = StringField(label='Image')
    store = QuerySelectField(label='Store', query_factory=store_query)
    submit = SubmitField(label='Create Item')
