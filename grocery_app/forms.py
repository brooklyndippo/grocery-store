from ast import Store
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, SubmitField, FloatField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, URL
from grocery_app.models import GroceryStore, ItemCategory

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
