from flask import Flask, render_template, request, redirect, url_for, session, flash
from forms import *
from user import *
from feedback import *
import shelve
from flask_wtf.csrf import CSRFProtect  # up for debate

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
    return render_template('shop.html')


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

        feedback = Feedback(email, phonenumber, name,message, count)

        feedback_dict[feedback.get_uid()] = feedback
        db['Feedback'] = feedback_dict
        db.close()
        return redirect(url_for("home"))
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


# Admin feedback View
@app.route('/admin/feedback')
def feedback():
    return render_template('admin/admin-users-feedback.html')


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


if __name__ == '__main__':
    app.run(debug=True)
