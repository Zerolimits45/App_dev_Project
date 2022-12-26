from wtforms import *


class loginUser(Form):
    email = EmailField("Email Address", [validators.Email(granular_message=True)], )
