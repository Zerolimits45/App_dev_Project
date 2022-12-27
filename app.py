from flask import Flask, render_template, request, redirect, url_for, session
from forms import *
from user import *
import shelve
from flask_wtf.csrf import CSRFProtect  # up for debate

app = Flask(__name__)
csrf = CSRFProtect(app)
app.secret_key = 'jiceuiruineruiferuifbwneionweicbuivbruinewicwebvuierniwndiwebciuevbiuerdniweoncueivbuiecbwuicbewui'


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/shop')
def shop():
    return render_template('shop.html')


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
            return redirect(url_for('home'))
        else:
            for key in user_dict:
                if form.email.data == user_dict[key].get_email():
                    user = user_dict[key]
                    session['CurrentUser'] = user.get_uid()
                    session.pop('Admin', None)
                    return redirect(url_for('home'))
    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
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

        return redirect(url_for('login'))
    return render_template('signUp.html', form=form)


@app.route('/logout')
def logout():
    session.pop('CurrentUser', None)
    session.pop('Admin', None)
    return redirect(url_for('home'))

@app.route('/admin/users')
def users():
    return render_template('admin/admin-home.html')

if __name__ == '__main__':
    app.run(debug=True)
