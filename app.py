from flask import Flask, render_template, request
from forms import loginForm

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/shop')
def shop():
    return render_template('shop.html')


@app.route('/login')
def login():
    form = loginForm(request.form)
    return render_template('login.html', form=form)


if __name__ == '__main__':
    app.run()
