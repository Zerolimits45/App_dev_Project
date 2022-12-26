from wtforms import *


# Login for users
class loginForm(Form):
    email = EmailField("Email Address", [
        validators.Email(granular_message=True),
        validators.DataRequired(message="Please input your email")
    ])
    password = PasswordField("Password", [
        validators.Length(6, 64, message="Password must be at least 6 characters"),
        validators.DataRequired(message="Please input your password")
    ])
