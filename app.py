from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
import os
from forms import *
from user import *
from feedback import *
import shelve
from flask_wtf.csrf import CSRFProtect  # up for debate
from Product import *
from Address import *
from Coupon import *
import stripe

app = Flask(__name__)
csrf = CSRFProtect(app)
app.secret_key = 'jiceuiruineruiferuifbwneionweicbuivbruinewicwebvuierniwndiwebciuevbiuerdniweoncueivbuiecbwuicbewui'
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
stripe.api_key = 'sk_test_51MSMj1Lg2iGcn067n1XTyiS8D8RgdUAL5Q6f8do538VuAejaeW1njfn1sBwSGquDR1O4OdtdkYWy7JdUq7WocQKQ006lGoXUiC'


# Home
@app.route('/')
def home():
    if 'Admin' in session:
        return redirect(url_for('users'))
    return render_template('index.html')


@app.route('/profile/<int:id>')
def profile(id):
    user_dict = {}
    db = shelve.open('Users')
    try:
        if 'User' in db:
            user_dict = db['User']
        else:
            db['User'] = user_dict
    except:
        print("Error in retrieving Users from storage.")
    db.close()

    user = user_dict.get(id)

    return render_template('profile/profile.html', user=user)


# View Address
@app.route('/profile/address')
def address():
    addresses_dict = {}
    db = shelve.open('Addresses')
    try:
        if 'Address' in db:
            addresses_dict = db['Address']
        else:
            db['Address'] = addresses_dict
    except:
        print("Error in retrieving Addresses from storage.")
    db.close()

    user_dict = {}
    db = shelve.open('Users')
    try:
        if 'User' in db:
            user_dict = db['User']
        else:
            db['User'] = user_dict
    except:
        print("Error in retrieving Users from storage.")
    db.close()

    addresses_list = []
    for key in addresses_dict:
        address = addresses_dict.get(key)
        addresses_list.append(address)

    user = user_dict.get(session['CurrentUser'])

    return render_template('profile/profile-addresses.html', addresses_list=addresses_list, user=user)


@app.route('/profile/edit/<int:id>', methods=['GET', 'POST'])
def profile_edit(id):
    form = EditProfileForm(id, request.form)
    if request.method == 'POST' and form.validate():
        user_dict = {}
        db = shelve.open('Users')
        try:
            if 'User' in db:
                user_dict = db['User']
            else:
                db['User'] = user_dict
        except:
            print("Error in retrieving Users from storage.")

        user = user_dict.get(id)
        user.set_email(form.email.data)
        user.set_name(form.name.data)

        db['User'] = user_dict
        db.close()
        return redirect(url_for('profile', id=id))
    else:
        user_dict = {}
        db = shelve.open('Users')
        try:
            if 'User' in db:
                user_dict = db['User']
            else:
                db['User'] = user_dict
        except:
            print("Error in retrieving Users from storage.")

        user = user_dict.get(id)
        form.email.data = user.get_email()
        form.name.data = user.get_name()

        db.close()
        flash('Edit Successfully')
    return render_template('profile/profile-user-edit.html', form=form, id=id)


# Contact
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm(request.form)
    if request.method == 'POST' and form.validate():
        feedback_dict = {}
        db = shelve.open('Feedbacks')
        try:
            if 'Feedback' in db:
                feedback_dict = db['Feedback']
            else:
                db['Feedback'] = feedback_dict
        except:
            print("Error in retrieving Feedbacks from storage.")
        email = form.email.data
        phonenumber = form.phonenumber.data
        name = form.name.data
        message = form.message.data
        count = len(feedback_dict)

        feedback = Feedback(email, phonenumber, name, message, count)

        feedback_dict[feedback.get_uid()] = feedback
        db['Feedback'] = feedback_dict
        db.close()
        return render_template('contact-success.html')
    return render_template('contact.html', form=form)


# Login
@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user_dict = {}
        db = shelve.open('Users')
        try:
            if 'User' in db:
                user_dict = db['User']
            else:
                db['User'] = user_dict
        except:
            print("Error in retrieving Users from storage.")
        db.close()
        if form.email.data == 'admin@mail.com' and form.password.data == 'password':
            session['Admin'] = form.email.data
            return redirect(url_for('users'))
        else:
            for key in user_dict:
                if form.email.data == user_dict[key].get_email():
                    user = user_dict[key]
                    session['CurrentUser'] = user.get_uid()
                    session['CurrentUsername'] = user.get_name()
                    session['CurrentUserEmail'] = user.get_email()
                    session['Cart'] = []
                    session['PreviousPrice'] = []
                    session.pop('Admin', None)
                    flash('Logged In Successfully')
                    return redirect(url_for('home'))
    return render_template('login.html', form=form)


# Session
@app.before_request
def make_session_permanent():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        if form.remember_me.data:
            session.permanent = True
        else:
            session.permanent = False


# Sign up
@app.route('/signup', methods=['GET', 'POST'])  # adding the new user after the sign-up
def signup():
    form = SignUpForm(request.form)
    if request.method == 'POST' and form.validate():
        user_dict = {}
        db = shelve.open('Users')
        try:
            if 'User' in db:
                user_dict = db['User']
            else:
                db['User'] = user_dict
        except:
            print("Error in retrieving Users from storage.")

        email = form.email.data
        password = form.password.data
        name = form.name.data
        count = len(user_dict)

        user = User(email, password, name, count)

        user_dict[user.get_uid()] = user
        db['User'] = user_dict

        db.close()
        flash('Signed Up Successfully')
        return redirect(url_for('login'))
    return render_template('signUp.html', form=form)


# Logout
@app.route('/logout')
def logout():
    session.pop('CurrentUser', None)
    session.pop('Admin', None)
    return redirect(url_for('home'))


# Add Address
@app.route('/profile/address/add', methods=['GET', 'POST'])
def add_address():
    form = addAddressForm(request.form)
    if request.method == 'POST' and form.validate():
        addresses_dict = {}
        db = shelve.open('Addresses')
        try:
            if 'Address' in db:
                addresses_dict = db['Address']
            else:
                db['Address'] = addresses_dict
        except:
            print("Error in retrieving Addresses from storage.")

        name = form.name.data
        location = form.location.data
        count = len(addresses_dict)

        address = Address(session['CurrentUser'], name, location, count)

        addresses_dict[address.getlocationid()] = address
        db['Address'] = addresses_dict

        db.close()
        flash('Added Successfully')
        return redirect(url_for('address'))
    return render_template('profile/profile-address-add.html', form=form)


# Edit Address
@app.route('/profile/address/edit/<int:id>', methods=['GET', 'POST'])
def edit_address(id):
    form = editAddressForm(request.form)
    if request.method == 'POST' and form.validate():
        addresses_dict = {}
        db = shelve.open('Addresses')
        try:
            if 'Address' in db:
                addresses_dict = db['Address']
            else:
                db['Address'] = addresses_dict
        except:
            print("Error in retrieving Addresses from storage.")

        address = addresses_dict.get(id)
        address.setname(form.name.data)
        address.setlocation(form.location.data)

        db['Address'] = addresses_dict
        db.close()
        return redirect(url_for('address', id=id))
    else:
        addresses_dict = {}
        db = shelve.open('Addresses')
        try:
            if 'Address' in db:
                addresses_dict = db['Address']
            else:
                db['Address'] = addresses_dict
        except:
            print("Error in retrieving Addresses from storage.")

        address = addresses_dict.get(id)
        form.name.data = address.getname()
        form.location.data = address.getlocation()

        db.close()
        flash('Edit Successfully')
    return render_template('profile/profile-address-edit.html', form=form)


# Delete Address
@app.route('/deleteaddress/<int:id>', methods=['GET', 'POST'])
def delete_address(id):
    addresses_dict = {}
    db = shelve.open('Addresses')
    try:
        if 'Address' in db:
            addresses_dict = db['Address']
        else:
            db['Address'] = addresses_dict
    except:
        print("Error in retrieving Addresses from storage.")

    addresses_dict.pop(id)
    db['Address'] = addresses_dict
    db.close()
    flash('Deleted Successfully')
    return redirect(url_for('address'))


@app.route('/shop/productdescription/<int:id>', methods=['GET', 'POST'])
def product_description(id):
    form = quantityForm(request.form)
    products_dict = {}
    db = shelve.open('Products', 'c')
    try:
        if 'Product' in db:
            products_dict = db['Product']
        else:
            db['Product'] = products_dict
    except:
        print("Error in retrieving Products from storage.")
    db.close()

    product = products_dict.get(id)
    cart_list = session['Cart']

    if request.method == 'POST' and form.validate():
        for i in cart_list:
            if i[0] == product.get_name():
                i[1] = form.quantity.data * product.get_price()
                i[2] = form.quantity.data
                session['Cart'] = cart_list
                flash('Item Changed In Cart')
                return redirect(url_for('cart'))

        cart = [product.get_name(), form.quantity.data * product.get_price(), form.quantity.data, product.get_image(), product.get_product_id()]
        session['Cart'].append(cart)
        flash('Added to Cart Successfully')
        return redirect(url_for('shop'))
    else:
        for i in cart_list:
            if i[4] == id:
                form.quantity.data = i[2]

        return render_template('shop_categories/product-description.html', form=form, product=product)


# Shop
@app.route('/shop')
def shop():
    products_dict = {}
    db = shelve.open('Products', 'c')
    try:
        if 'Product' in db:
            products_dict = db['Product']
        else:
            db['Product'] = products_dict
    except:
        print("Error in retrieving Products from storage.")
    db.close()

    products_list = []
    for key in products_dict:
        product = products_dict.get(key)
        if product.get_brand() == 'Seiko':
            products_list.append(product)

    return render_template('shop_categories/shop.html', products_list=products_list)


@app.route('/shop/casio')
def casio():
    products_dict = {}
    db = shelve.open('Products', 'c')
    try:
        if 'Product' in db:
            products_dict = db['Product']
        else:
            db['Product'] = products_dict
    except:
        print("Error in retrieving Products from storage.")
    db.close()

    products_list = []
    for key in products_dict:
        product = products_dict.get(key)
        if product.get_brand() == 'Casio':
            products_list.append(product)

    return render_template('shop_categories/shop-casio.html', products_list=products_list)


@app.route('/shop/orient')
def orient():
    products_dict = {}
    db = shelve.open('Products', 'c')
    try:
        if 'Product' in db:
            products_dict = db['Product']
        else:
            db['Product'] = products_dict
    except:
        print("Error in retrieving Products from storage.")
    db.close()

    products_list = []
    for key in products_dict:
        product = products_dict.get(key)
        if product.get_brand() == 'Orient':
            products_list.append(product)

    return render_template('shop_categories/shop-orient.html', products_list=products_list)


@app.route('/shop/tag')
def tag():
    products_dict = {}
    db = shelve.open('Products', 'c')
    try:
        if 'Product' in db:
            products_dict = db['Product']
        else:
            db['Product'] = products_dict
    except:
        print("Error in retrieving Products from storage.")
    db.close()

    products_list = []
    for key in products_dict:
        product = products_dict.get(key)
        if product.get_brand() == 'TAG Heuer':
            products_list.append(product)

    return render_template('shop_categories/shop-tag.html', products_list=products_list)


@app.route('/shop/rolex')
def rolex():
    products_dict = {}
    db = shelve.open('Products', 'c')
    try:
        if 'Product' in db:
            products_dict = db['Product']
        else:
            db['Product'] = products_dict
    except:
        print("Error in retrieving Products from storage.")
    db.close()

    products_list = []
    for key in products_dict:
        product = products_dict.get(key)
        if product.get_brand() == 'Rolex':
            products_list.append(product)

    return render_template('shop_categories/shop-rolex.html', products_list=products_list)


@app.route('/cart')
def cart():
    cart_list = session['Cart']

    if len(session['PreviousPrice']) > 0:
        if 'CouponApplied' in session:
            for i, j in zip(cart_list, session['PreviousPrice']):
                i[1] = j
                session['Cart'] = cart_list
            session.pop('CouponApplied', None)

    if len(cart_list) > 0:
        session['PreviousPrice'] = [i[1] for i in cart_list]

    return render_template('cart.html')


# Remove cart item
@app.route('/removeitem/<int:id>', methods=['GET', 'POST'])
def remove_item(id):
    session['Cart'].pop(id - 1)
    flash('Removed Item')
    return redirect(url_for('cart'))


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if len(session['Cart']) == 0:
        flash('Cart is Empty')
        return redirect(url_for('cart'))

    addresses_dict = {}
    db = shelve.open('Addresses')
    try:
        if 'Address' in db:
            addresses_dict = db['Address']
        else:
            db['Address'] = addresses_dict
    except:
        print("Error in retrieving Addresses from storage.")
    db.close()

    user_dict = {}
    db = shelve.open('Users')
    try:
        if 'User' in db:
            user_dict = db['User']
        else:
            db['User'] = user_dict
    except:
        print("Error in retrieving Users from storage.")
    db.close()

    addresses_list = []
    for key in addresses_dict:
        address = addresses_dict.get(key)
        addresses_list.append(address)

    user = user_dict.get(session['CurrentUser'])

    return render_template('checkout.html', addresses_list=addresses_list, user=user)


@app.route('/payment/<int:lid>/<int:id>', methods=['GET', 'POST'])
def payment(lid, id):
    addresses_dict = {}
    db = shelve.open('Addresses')
    try:
        if 'Address' in db:
            addresses_dict = db['Address']
        else:
            db['Address'] = addresses_dict
    except:
        print("Error in retrieving Addresses from storage.")
    db.close()

    coupons_dict = {}
    db = shelve.open('Coupons', 'c')
    try:
        if 'Coupon' in db:
            coupons_dict = db['Coupon']
        else:
            db['Coupon'] = coupons_dict
    except:
        print("Error in retrieving Coupons from Storage")
    db.close()

    user_dict = {}
    db = shelve.open('Users', 'c')
    try:
        if 'User' in db:
            user_dict = db['User']
        else:
            db['User'] = user_dict
    except:
        print("Error in retrieving Users from storage.")

    address = addresses_dict.get(lid)
    user = user_dict.get(id)
    coupons_list = []
    for i in user.get_coupons():
        coupons_list.append(coupons_dict.get(i))

    total_amount = []
    for product in session['Cart']:
        total_amount.append(product[1])

    cart_list = session['Cart']
    form = ApplyCouponForm(request.form)
    form.coupons.choices = [('0', 'Select')] + [(i.get_id(), i.get_name()) for i in coupons_list]
    if request.method == "POST" and form.validate():
        for coupon in coupons_list:
            if int(form.coupons.data) == coupon.get_id():
                for i, j in zip(cart_list, session['PreviousPrice']):
                    i[1] = j
                    i[1] *= (1-coupon.get_effect())
                    i[1] = int(i[1])
                    session['Cart'] = cart_list
                    session['CouponApplied'] = coupon.get_id()
                return redirect(url_for('payment', id=id))

            elif int(form.coupons.data) == 0:
                for i, j in zip(cart_list, session['PreviousPrice']):
                    i[1] = j
                    session['Cart'] = cart_list
                    session['CouponApplied'] = 0
                return redirect(url_for('payment', id=id))
    else:
        if 'CouponApplied' in session:
            form.coupons.default = str(session['CouponApplied'])
            form.process()

    return render_template('payment.html', address=address, total_amount=total_amount, form=form)


@app.route('/stripe_payment/<int:lid>/<int:id>', methods=['GET', 'POST'])
def stripe_payment(lid, id):
    line_items_list = []
    for item in session['Cart']:
        if item[2] > 1:
            item[1] = int(item[1] / item[2])
            line_item = {"price_data": {"product_data": {"name": item[0]}, "currency": 'sgd', "unit_amount": item[1]*100}, "quantity": item[2]}
        else:
            line_item = {"price_data": {"product_data": {"name": item[0]}, "currency": 'sgd', "unit_amount": item[1]*100}, "quantity": item[2]}
        line_items_list.append(dict(line_item))

    checkout_session = stripe.checkout.Session.create(
        line_items=line_items_list,
        payment_method_types=['card'],
        mode='payment',
        success_url=request.host_url + 'stripe-success/' + str(id),
        cancel_url=request.host_url + 'payment/' + str(lid) + '/' + str(id),
    )
    return redirect(checkout_session.url)


@app.route('/stripe-success/<int:id>')
def stripe_success(id):
    user_dict = {}
    db = shelve.open('Users', 'c')
    try:
        if 'User' in db:
            user_dict = db['User']
        else:
            db['User'] = user_dict
    except:
        print("Error in retrieving Users from storage.")

    user = user_dict.get(id)
    total_amount = []
    for product in session['Cart']:
        total_amount.append(product[1])

    user.set_money_spent(sum(total_amount))
    user.set_points()
    if 'CouponApplied' in session:
        user.get_coupons().pop(session['CouponApplied'], None)

    db['User'] = user_dict
    db.close()

    products_dict = {}
    db = shelve.open('Products', 'c')
    try:
        if 'Product' in db:
            products_dict = db['Product']
        else:
            db['Product'] = products_dict
    except:
        print("Error in retrieving Products from storage.")

    for item in session['Cart']:
        product = products_dict.get(item[4])
        product.set_quantity((product.get_quantity() - int(item[2])))

    db['Product'] = products_dict
    db.close()

    return render_template('stripe_success.html')


@app.route('/rewards/<int:id>')
def rewards(id):
    user_dict = {}
    db = shelve.open('Users', 'c')
    try:
        if 'User' in db:
            user_dict = db['User']
        else:
            db['User'] = user_dict
    except:
        print("Error in retrieving Users from storage.")

    user = user_dict.get(id)
    db['User'] = user_dict
    db.close()

    coupons_dict = {}
    db = shelve.open('Coupons', 'c')
    try:
        if 'Coupon' in db:
            coupons_dict = db['Coupon']
        else:
            db['Coupon'] = coupons_dict
    except:
        print("Error in retrieving Coupons from Storage")
    db.close()

    coupons_list = []
    for key in coupons_dict:
        coupon = coupons_dict.get(key)
        for i in user.get_coupons():
            if coupon.get_id() == i:
                coupons_list.append(coupon)

    return render_template('rewards.html', user=user, coupons_list=coupons_list)


@app.route('/rewards/redeem/<int:id>')
def redeem(id):
    user_dict = {}
    db = shelve.open('Users', 'c')
    try:
        if 'User' in db:
            user_dict = db['User']
        else:
            db['User'] = user_dict
    except:
        print("Error in retrieving Users from storage.")
    db.close()

    user = user_dict.get(id)

    coupons_dict = {}
    db = shelve.open('Coupons', 'c')
    try:
        if 'Coupon' in db:
            coupons_dict = db['Coupon']
        else:
            db['Coupon'] = coupons_dict
    except:
        print("Error in retrieving Coupons from Storage")
    db.close()

    coupons_list = []
    for key in coupons_dict:
        coupon = coupons_dict.get(key)
        if coupon.get_id() not in user.get_coupons():
            coupons_list.append(coupon)

    return render_template('rewards-redeem.html', user=user, coupons_list=coupons_list)


@app.route('/rewards/redeem-reward/<int:id>/<int:cid>', methods=['GET', 'POST'])
def redeem_reward(id, cid):
    coupons_dict = {}
    db = shelve.open('Coupons', 'c')
    try:
        if 'Coupon' in db:
            coupons_dict = db['Coupon']
        else:
            db['Coupon'] = coupons_dict
    except:
        print("Error in retrieving Coupons from Storage")
    db.close()

    user_dict = {}
    db = shelve.open('Users', 'c')
    try:
        if 'User' in db:
            user_dict = db['User']
        else:
            db['User'] = user_dict
    except:
        print("Error in retrieving Users from storage.")

    user = user_dict.get(id)
    coupon = coupons_dict.get(cid)
    user.set_coupons(cid)
    user.set_points(user.get_points() - coupon.get_price())
    db['User'] = user_dict
    db.close()

    return redirect(url_for('rewards', id=id))


# Admin side
# ====================================================================================================================
# Admin user view
@app.route('/admin/users', methods=['GET', 'POST'])
def users():
    user_dict = {}
    db = shelve.open('Users', 'c')
    try:
        if 'User' in db:
            user_dict = db['User']
        else:
            db['User'] = user_dict
    except:
        print("Error in retrieving Users from storage.")
    db.close()

    users_list = []
    for key in user_dict:
        user = user_dict.get(key)
        users_list.append(user)

    form = SortUserForm(request.form)
    if request.method == "POST" and form.validate():
        if form.sort.data == "Ascending":
            users_list.sort(key=lambda x: x.get_points())
        elif form.sort.data == "Descending":
            users_list.sort(key=lambda x: x.get_points(), reverse=True)

    return render_template('admin/admin-home.html', count=len(users_list), users_list=users_list, form=form)


# Admin edit users
@app.route('/admin/users/edit/<int:id>', methods=['GET', 'POST'])
def editUsers(id):
    form = EditUserForm(id, request.form)
    if request.method == 'POST' and form.validate():
        user_dict = {}
        db = shelve.open('Users')
        try:
            if 'User' in db:
                user_dict = db['User']
            else:
                db['User'] = user_dict
        except:
            print("Error in retrieving Users from storage.")

        user = user_dict.get(id)
        user.set_email(form.email.data)
        user.set_name(form.name.data)

        db['User'] = user_dict
        db.close()
        return redirect(url_for('users'))
    else:
        user_dict = {}
        db = shelve.open('Users')
        try:
            if 'User' in db:
                user_dict = db['User']
            else:
                db['User'] = user_dict
        except:
            print("Error in retrieving Users from storage.")

        user = user_dict.get(id)
        form.email.data = user.get_email()
        form.name.data = user.get_name()

        db.close()
        flash('Edit Successfully')
        return render_template('admin/admin-user-edit.html', form=form)


# Admin Delete User
@app.route('/deleteuser/<int:id>', methods=['GET', 'POST'])
def delete_user(id):
    user_dict = {}
    db = shelve.open('Users')
    try:
        if 'User' in db:
            user_dict = db['User']
        else:
            db['User'] = user_dict
    except:
        print("Error in retrieving Users from storage.")

    user_dict.pop(id)
    db['User'] = user_dict
    db.close()
    flash('Deleted Successfully')
    return redirect(url_for('users'))


# Admin Product View
@app.route('/admin/product', methods=['GET', 'POST'])
def products():
    products_dict = {}
    db = shelve.open('Products', 'c')
    try:
        if 'Product' in db:
            products_dict = db['Product']
        else:
            db['Product'] = products_dict
    except:
        print("Error in retrieving Products from storage.")
    db.close()

    products_list = []
    for key in products_dict:
        product = products_dict.get(key)
        products_list.append(product)

    form = SortProductForm(request.form)
    if request.method == "POST" and form.validate():
        if form.sort.data == "Price":
            if form.direction.data == "Ascending":
                products_list.sort(key=lambda x: x.get_price())
            elif form.direction.data == "Descending":
                products_list.sort(key=lambda x: x.get_price(), reverse=True)
        elif form.sort.data == "Quantity":
            if form.direction.data == "Ascending":
                products_list.sort(key=lambda x: x.get_quantity())
            elif form.direction.data == "Descending":
                products_list.sort(key=lambda x: x.get_quantity(), reverse=True)

    return render_template('admin/admin-products.html', products_list=products_list, form=form)


# Admin Product Edit
@app.route('/admin/product/edit/<int:id>', methods=['GET', 'POST'])
def edit_products(id):
    form = EditProductForm()
    if request.method == 'POST' and form.validate():
        products_dict = {}
        db = shelve.open('Products', 'c')
        try:
            if 'Product' in db:
                products_dict = db['Product']
            else:
                db['Product'] = products_dict
        except:
            print("Error in retrieving Products from storage.")

        product = products_dict.get(id)
        product.set_name(form.name.data)
        product.set_price(form.price.data)
        product.set_quantity(form.quantity.data)
        product.set_description(form.description.data)
        product.set_brand(form.brand.data)

        file = form.image.data
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            product.set_image(filename)

        db['Product'] = products_dict
        db.close()
        flash('Edit Successfully')
        return redirect(url_for('products'))
    else:
        products_dict = {}
        db = shelve.open('Products', 'c')
        try:
            if 'Product' in db:
                products_dict = db['Product']
            else:
                db['Product'] = products_dict
        except:
            print("Error in retrieving Products from storage.")

        product = products_dict.get(id)
        form.name.data = product.get_name()
        form.price.data = product.get_price()
        form.description.data = product.get_description()
        form.quantity.data = product.get_quantity()
        form.brand.data = product.get_brand()

        db.close()

        return render_template('admin/admin-products-edit.html', form=form, product=product)


# Admin Add Product
@app.route('/admin/product/add', methods=['GET', 'POST'])
def create_products():
    form = CreateProductForm()
    if request.method == 'POST' and form.validate():
        products_dict = {}
        db = shelve.open('Products', 'c')
        try:
            if 'Product' in db:
                products_dict = db['Product']
            else:
                db['Product'] = products_dict
        except:
            print("Error in retrieving Products from storage.")

        file = form.image.data
        if file:
            name = form.name.data
            price = form.price.data
            description = form.description.data
            brand = form.brand.data
            quantity = form.quantity.data
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            count = len(products_dict)
            product = Product(name, price, description, brand, quantity, filename, count)
        else:
            name = form.name.data
            price = form.price.data
            description = form.description.data
            brand = form.brand.data
            quantity = form.quantity.data
            filename = None
            count = len(products_dict)
            product = Product(name, price, description, brand, quantity, filename, count)

        products_dict[product.get_product_id()] = product
        db['Product'] = products_dict

        db.close()
        return redirect(url_for('products'))
    return render_template('admin/admin-products-add.html', form=form)


# Admin Delete Product
@app.route('/deleteproduct/<int:id>', methods=['GET', 'POST'])
def delete_product(id):
    products_dict = {}
    db = shelve.open('Products', 'c')
    try:
        if 'Product' in db:
            products_dict = db['Product']
        else:
            db['Product'] = products_dict
    except:
        print("Error in retrieving Products from storage.")

    products_dict.pop(id)
    db['Product'] = products_dict
    db.close()
    flash('Deleted Successfully')
    return redirect(url_for('products'))


# Admin feedback View
@app.route('/admin/feedback')
def feedback():
    feedback_dict = {}
    db = shelve.open('Feedbacks', 'c')
    try:
        if 'Feedback' in db:
            feedback_dict = db['Feedback']
        else:
            db['Feedback'] = feedback_dict
    except:
        print("Error in retrieving Feedbacks from storage.")
    db.close()

    feedbacks_list = []
    for key in feedback_dict:
        feedback = feedback_dict.get(key)
        feedbacks_list.append(feedback)

    return render_template('admin/admin-users-feedback.html', count=len(feedbacks_list), feedbacks_list=feedbacks_list)


# Admin Delete Feedback
@app.route('/deletefeedback/<int:id>', methods=['GET', 'POST'])
def delete_feedback(id):
    feedback_dict = {}
    db = shelve.open('Feedbacks', 'c')
    try:
        if 'Feedback' in db:
            feedback_dict = db['Feedback']
        else:
            db['Feedback'] = feedback_dict
    except:
        print("Error in retrieving Feedbacks from storage.")

    feedback_dict.pop(id)
    db['Feedback'] = feedback_dict
    db.close()
    flash('Deleted Successfully')
    return redirect(url_for('feedback'))


@app.route('/admin/coupons', methods=['GET', 'POST'])
def coupons():
    coupons_dict = {}
    db = shelve.open('Coupons', 'c')
    try:
        if 'Coupon' in db:
            coupons_dict = db['Coupon']
        else:
            db['Coupon'] = coupons_dict
    except:
        print("Error in retrieving Coupons from Storage")
    db.close()

    coupons_list = []
    for key in coupons_dict:
        coupon = coupons_dict.get(key)
        coupons_list.append(coupon)

    form = SortCouponForm(request.form)
    if request.method == "POST" and form.validate():
        if form.sort.data == "Price":
            if form.direction.data == "Ascending":
                coupons_list.sort(key=lambda x: x.get_price())
            elif form.direction.data == "Descending":
                coupons_list.sort(key=lambda x: x.get_price(), reverse=True)
        elif form.sort.data == "Effect":
            if form.direction.data == "Ascending":
                coupons_list.sort(key=lambda x: x.get_effect())
            elif form.direction.data == "Descending":
                coupons_list.sort(key=lambda x: x.get_effect(), reverse=True)

    return render_template('admin/admin-coupons.html', coupons_list=coupons_list, form=form)


@app.route('/admin/coupons/edit/<int:id>', methods=['GET', 'POST'])
def edit_coupon(id):
    form = editCouponForm(request.form)
    if request.method == "POST" and form.validate():
        coupons_dict = {}
        db = shelve.open('Coupons', 'c')
        try:
            if 'Coupon' in db:
                coupons_dict = db['Coupon']
            else:
                db['Coupon'] = coupons_dict
        except:
            print("Error in retrieving Coupons from Storage")

        coupon = coupons_dict.get(id)
        coupon.set_name(form.name.data)
        coupon.set_price(form.price.data)
        coupon.set_effect(form.effect.data)

        db['Coupon'] = coupons_dict
        db.close()
        return redirect(url_for('coupons'))
    else:
        coupons_dict = {}
        db = shelve.open('Coupons', 'c')
        try:
            if 'Coupon' in db:
                coupons_dict = db['Coupon']
            else:
                db['Coupon'] = coupons_dict
        except:
            print("Error in retrieving Coupons from Storage")

        coupon = coupons_dict.get(id)
        form.name.data = coupon.get_name()
        form.price.data = coupon.get_price()
        form.effect.data = coupon.get_effect()

        db.close()
        flash('Edit Successfully')
    return render_template('admin/admin-coupons-edit.html', form=form)


@app.route('/admin/coupons/add', methods=['GET', 'POST'])
def add_coupon():
    form = addCouponForm(request.form)
    if request.method == "POST" and form.validate():
        coupons_dict = {}
        db = shelve.open('Coupons', 'c')
        try:
            if 'Coupon' in db:
                coupons_dict = db['Coupon']
            else:
                db['Coupon'] = coupons_dict
        except:
            print("Error in retrieving Coupons from Storage")

        name = form.name.data
        price = form.price.data
        effect = form.effect.data
        count = len(coupons_dict)

        coupon = Coupon(name, price, effect, count)

        coupons_dict[coupon.get_id()] = coupon
        db['Coupon'] = coupons_dict

        db.close()
        flash('Added Successfully')
        return redirect(url_for('coupons'))

    return render_template('admin/admin-coupons-add.html', form=form)


@app.route('/admin/deletecoupon/<int:id>', methods=['GET', 'POST'])
def delete_coupon(id):
    coupons_dict = {}
    db = shelve.open('Coupons', 'c')
    try:
        if 'Coupon' in db:
            coupons_dict = db['Coupon']
        else:
            db['Coupon'] = coupons_dict
    except:
        print("Error in retrieving Coupons from Storage")

    coupons_dict.pop(id)
    db['Coupon'] = coupons_dict
    db.close()
    flash('Deleted Successfully')

    return redirect(url_for('coupons'))


@app.route('/admin/users/address/<int:id>', methods=['GET', 'POST'])
def user_address(id):
    addresses_dict = {}
    db = shelve.open('Addresses')
    try:
        if 'Address' in db:
            addresses_dict = db['Address']
        else:
            db['Address'] = addresses_dict
    except:
        print("Error in retrieving Addresses from storage.")
    db.close()

    user_dict = {}
    db = shelve.open('Users')
    try:
        if 'User' in db:
            user_dict = db['User']
        else:
            db['User'] = user_dict
    except:
        print("Error in retrieving Users from storage.")
    db.close()

    addresses_list = []
    for key in addresses_dict:
        address = addresses_dict.get(key)
        addresses_list.append(address)

    user = user_dict.get(id)

    return render_template('admin/admin-user-address.html', user=user, addresses_list=addresses_list)


if __name__ == '__main__':
    app.run(debug=True)
