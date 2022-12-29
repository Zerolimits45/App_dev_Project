from wtforms import Form, BooleanField, PasswordField, StringField, SelectField, SubmitField, TextAreaField, TelField, validators, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length, regexp
import shelve


# Login for users
class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired(message='Please input your email'), Email()])
    password = PasswordField('Password', validators=[DataRequired(message='Please input your password'),
                                                     Length(min=6, max=64,
                                                            message='Password must be at least 6 characters')])
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

        email_list = []
        for key in user_dict:
            email_list.append(user_dict[key].get_email())

        if self.email.data not in email_list and self.email.data != 'admin@mail.com':
            raise ValidationError('Incorrect Email or Password')


# Sign up for users
class SignUpForm(Form):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=64,message="Password needs to be at least 6 characters long.")])
    confirmPassword = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
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

        for key in user_dict:
            if self.email.data == user_dict[key].get_email():
                raise ValidationError('Email is already in use.')


# add product form
class CreateProductForm(Form):
    name = StringField('Name', validators=[DataRequired(message='Please input a product name.')])
    price = IntegerField('Price', validators=[DataRequired(message="Price needs to be a number."), ])
    description = TextAreaField('Description', validators=[validators.Optional()])
    quantity = IntegerField('Quantity', validators=[DataRequired(message="Quantity needs to be a number.")])
    add = SubmitField('Add')


# edit product form

class EditProductForm(Form):
    name = StringField('Name', validators=[DataRequired(message='Please input a product name.')])
    price = IntegerField('Price', validators=[DataRequired(message="Price needs to be a number."), ])
    description = TextAreaField('Description', validators=[validators.Optional()])
    quantity = IntegerField('Quantity', validators=[DataRequired(message="Quantity needs to be a number.")])
    save = SubmitField('Save')


# Contact Form
class ContactForm(Form):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phonenumber = StringField("Phone Number", validators=[regexp("^[689]\d{7}$", message="Please enter a valid phone number")])
    message = TextAreaField('Explain your Problem', validators=[DataRequired(), Length(min=1, max=1024, message="Please leave a message within 1024 characters")])
    submit = SubmitField('Send Feedback')


# Edit User Form
class EditUserForm(Form):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Save')

    def __init__(self, user_id, *args, **kwargs):
        super(EditUserForm, self).__init__(*args, **kwargs)
        self.user_id = user_id

    def validate_email(self, email):
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

        current_user = user_dict[self.user_id].get_email()
        for key in user_dict:
            if self.email.data == user_dict[key].get_email() and self.email.data != current_user:
                raise ValidationError('Email is already in use.')
