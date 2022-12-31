from flask import Flask, render_template, request, redirect, url_for, session, flash
from forms import *
from user import *
from feedback import *
import shelve
from flask_wtf.csrf import CSRFProtect  # up for debate
from Product import *
from Address import *

app = Flask(__name__)
csrf = CSRFProtect(app)
app.secret_key = 'jiceuiruineruiferuifbwneionweicbuivbruinewicwebvuierniwndiwebciuevbiuerdniweoncueivbuiecbwuicbewui'


# Home
@app.route('/')
def home():
    if 'Admin' in session:
        return redirect(url_for('users'))
    return render_template('index.html')


# Shop
@app.route('/shop')
def shop():
    return render_template('shop_categories/shop.html')


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


@app.route('/shop/productdescription')
def product_description():
    form = quantityForm(request.form)
    return render_template('shop_categories/product-description.html',form=form)


@app.route('/shop/casio')
def casio():
    return render_template('shop_categories/shop-casio.html')


@app.route('/shop/orient')
def orient():
    return render_template('shop_categories/shop-orient.html')


@app.route('/shop/tag')
def tag():
    return render_template('shop_categories/shop-tag.html')


@app.route('/shop/rolex')
def rolex():
    return render_template('shop_categories/shop-rolex.html')


# Admin side
# ====================================================================================================================
# Admin user view
@app.route('/admin/users')
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

    return render_template('admin/admin-home.html', count=len(users_list), users_list=users_list)


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
@app.route('/admin/product')
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

    return render_template('admin/admin-products.html', products_list=products_list)


# Admin Product Edit
@app.route('/admin/product/edit/<int:id>', methods=['GET', 'POST'])
def edit_products(id):
    form = CreateProductForm(request.form)
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

        return render_template('admin/admin-products-edit.html', form=form)


# Admin Add Product
@app.route('/admin/product/add', methods=['GET', 'POST'])
def create_products():
    form = CreateProductForm(request.form)
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

        name = form.name.data
        price = form.price.data
        description = form.description.data
        brand = form.brand.data
        quantity = form.quantity.data
        count = len(products_dict)

        product = Product(name, price, description, brand, quantity, None, count)
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


if __name__ == '__main__':
    app.run(debug=True)
