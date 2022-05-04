from flask import Blueprint, request, render_template, redirect, url_for, flash
from datetime import date, datetime
from grocery_app.models import GroceryStore, GroceryItem, User
from grocery_app.forms import GroceryStoreForm, GroceryItemForm, LoginForm, SignUpForm
from grocery_app import bcrypt
from flask_login import login_user, logout_user, login_required, current_user

# Import app and db from events_app package so that we can run app
from grocery_app.extensions import app, db

main = Blueprint("main", __name__)
auth = Blueprint("auth", __name__)

##########################################
#           Routes                       #
##########################################

@main.route('/')
def homepage():
    all_stores = GroceryStore.query.all()
    print(all_stores)
    return render_template('home.html', all_stores=all_stores)

@main.route('/new_store', methods=['GET', 'POST'])
def new_store():
    form = GroceryStoreForm()

    if form.validate_on_submit(): 
        store = GroceryStore(
            title = form.title.data,
            address = form.address.data,
            created_by=current_user
        )
        db.session.add(store)
        db.session.commit()
        flash('Succes! You created a new grocery store.')
        
        return redirect(url_for('main.store_detail', store_id=store.id))

    return render_template('new_store.html', form=form, form_title='New Store')

@main.route('/new_item', methods=['GET', 'POST'])
def new_item():
    form = GroceryItemForm()

    if form.validate_on_submit():
        item = GroceryItem(
            name=form.name.data,
            price=form.price.data,
            category=form.category.data,
            photo_url=form.photo_url.data,
            store=form.store.data,
            created_by=current_user
        )
        db.session.add(item)
        db.session.commit()
        flash('Succes! You created a new grocery item.')
        return redirect(url_for('main.item_detail', item_id=item.id))

    return render_template('new_item.html', form=form, form_title='New Item')

@main.route('/store/<store_id>', methods=['GET', 'POST'])
def store_detail(store_id):
    store = GroceryStore.query.get(store_id)
    form = GroceryStoreForm(obj=store)

    if form.validate_on_submit():
        store.title = form.title.data
        store.address = form.address.data

        db.session.commit()
        flash('Store Updated.')
        return redirect(url_for('main.store_detail', store_id=store.id))

    return render_template('store_detail.html', form=form, form_title='Edit Store', store=store)

@main.route('/item/<item_id>', methods=['GET', 'POST'])
def item_detail(item_id):

    item = GroceryItem.query.get(item_id)
    form = GroceryItemForm(obj=item)

    if form.validate_on_submit():
        item.name = form.name.data
        item.price = form.price.data
        item.category = form.category.data
        item.photo_url = form.photo_url.data
        item.store = form.store.data

        db.session.commit()
        flash('Grocery item updated.')
        return redirect(url_for('main.item_detail', item_id=item.id))

    return render_template('item_detail.html', form=form, form_title='Edit Item', item=item)

@main.route('/add_to_shopping_list/<item_id>', methods=['POST'])
def add_to_shopping_list(item_id):
    item = GroceryItem.query.get(item_id)
    user = current_user
    
    user.shopping_list_items.append(item)
    db.session.commit()
    flash('Succes! You added a new grocery item to your list.')
    return redirect(url_for('main.shopping_list'))


@main.route('/shopping_list')
@login_required
def shopping_list():
    user = current_user  
    return render_template('shopping_list.html', user=user)
    

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    print('in signup')
    form = SignUpForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username=form.username.data,
            password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash('Account Created.')
        print('created')
        return redirect(url_for('auth.login'))
    print(form.errors)
    return render_template('signup.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        login_user(user, remember=True)
        next_page = request.args.get('next')
        return redirect(next_page if next_page else url_for('main.homepage'))
    return render_template('login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.homepage'))