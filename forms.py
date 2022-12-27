from wtforms import Form, BooleanField, PasswordField, StringField, SelectField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
import shelve


# Login for users
class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired(message='Please input your email'), Email()])
    password = PasswordField('Password', validators=[DataRequired(message='Please input your password'), Length(min=6, max=64, message='Password must be at least 6 characters')])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')

    def validate_password(self, password):
        user_list = []
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

        id = None
        for key in user_dict:
            user_pair = []
            user_pair.append(user_dict[key].get_email())
            user_pair.append(user_dict[key].get_password())
            user_list.append(user_pair)

        for i in user_list:
            if self.email.data == i[0]:
                id = i

        if id != None:
            if self.password.data != id[1]:
                raise ValidationError('Incorrect Email or Password')

# Sign up for users

