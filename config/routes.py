from .init import app, db, bcrypt, login_manager
from .models import *
from .authform import *
from flask import flash, render_template, redirect, session, url_for, request
from flask_login import current_user, login_user, login_required, logout_user, UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#Authenticating user
@app.get('/register')
def signup():
    return render_template('register.html')

@app.post('/register')
def register_page():
    if current_user.is_authenticated:
        redirect(url_for('home'))
    form = RegisterForm()

    if form.validate_on_submit():
        password = bcrypt.generate_password_hash(form.password.data)
        user = User(
            name = form.name.data,
            email = form.email.data,
            balance = form.balance.data,
            password_hash = password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', title = 'Register')


@app.route('/login')
def login():
    return render_template('login.html')

@app.route("/login", methods=['POST'])
def login_page():
    if current_user.is_authenticated:
        redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('home'))
        else:
                flash("Invalid Username or password!", "danger")
        
    return render_template('login.html', title = 'Login')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


# Routes
@app.route('/')
@app.route('/home', methods=['GET'])
def home():
    products = Item.query.order_by(Item.name.desc())
    return render_template('home.html', products = products)

# add item
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        description = request.form['description']
        item = Item(name = name, price = price, description = description, buyer_id = 1)
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('add'))
    else:
        return render_template('add.html')
    

@app.route('/cart', methods=['POST','GET'])
def cart():
    total = 0
    cartItems = CartItem.query.filter_by(user_id = 1)
    if cartItems:
        for i in cartItems:
            item_info = Item.query.filter_by(id = i.id).first()
            total += item_info.price * i.quantity  
    return render_template('cart.html', cartItems = cartItems, total = total)

@app.route('/add_to_cart', methods = ['POST'])
def add_to_cart():
    if request.method == 'POST':
        item_id = request.form['id']
        quantity = request.form['quantity']
        cart_item = CartItem(item_id = item_id, user_id = current_user.get_id(), quantity = quantity)
        db.session.add(cart_item)
        db.session.commit()
        return redirect(url_for('add'))
    else:
        return render_template('add.html')

@app.route('/cart/remove/<int:item_id>')
def remove(item_id):
    cartItem = CartItem.query.get_or_404(item_id)
    db.session.delete(cartItem)
    db.session.commit()
    return render_template('cart.html')


@app.route('/cart/update/<int:id>', methods = ['GET', 'POST'])
def update_cart_item(id):
    qty = request.form['new_qty']
    cart_item = CartItem.query.get_or_404(id)
    if request.method == 'POST':
        if qty == 0:
            db.session.delete(cart_item)
        else:
            cart_item.quantity = qty
    db.session.commit()
    return render_template('cart.html')

# # view all items
# @app.route('/view')
# def view():
#     items = Item.query.all()
#     return render_template('view.html', items=items)

# # delete item
# @app.route('/delete/<int:id>')
# def delete(id):
#     item = Item.query.get_or_404(id)
#     db.session.delete(item)
#     db.session.commit()
#     return redirect(url_for('view'))

# # update item
# @app.route('/update/<int:id>', methods=['GET', 'POST'])
# def update(id):
#     item = Item.query.get_or_404(id)

#     # if a form is submitted
#     if request.method == 'POST':
#         item.name = request.form['name']
#         db.session.commit()
#         return redirect(url_for('view'))
#     # if a user is going to the page
#     else:
#         return render_template('update.html', item=item)

