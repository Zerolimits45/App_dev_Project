from wtforms import Form, BooleanField, PasswordField, StringField, SelectField, SubmitField, TextAreaField, TelField, \
    validators, IntegerField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length, regexp
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
import shelve
import geocoder


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
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=64,
                                                                            message="Password needs to be at least 6 characters long.")])
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
class CreateProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(message='Please input a product name.')])
    price = IntegerField('Price', validators=[DataRequired(message="Price needs to be a number."), ])
    description = TextAreaField('Description', validators=[validators.Optional()])
    brand = SelectField('Brand', validators=[DataRequired()],
                        choices=[('', 'Select'), ('Seiko', 'Seiko'), ('Orient', 'Orient'), ('Casio', 'Casio'),
                                 ('TAG Heuer', 'Tag Heuer'), ('Rolex', 'Rolex')], default='')
    quantity = IntegerField('Quantity', validators=[DataRequired(message="Quantity needs to be a number.")])
    image = FileField('Image', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'File not Supported, Images Only')])
    add = SubmitField('Add')


# edit product form

class EditProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(message='Please input a product name.')])
    price = IntegerField('Price', validators=[DataRequired(message="Price needs to be a number."), ])
    description = TextAreaField('Description', validators=[validators.Optional()])
    brand = SelectField('Brand', validators=[DataRequired()],
                        choices=[('', 'Select'), ('Seiko', 'Seiko'), ('Orient', 'Orient'), ('Casio', 'Casio'),
                                 ('TAG Heuer', 'Tag Heuer'), ('Rolex', 'Rolex')], default='')
    quantity = IntegerField('Quantity', validators=[DataRequired(message="Quantity needs to be a number.")])
    image = FileField('Image', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'File not Supported, Images Only')])
    save = SubmitField('Save')


# Contact Form
class ContactForm(Form):
    name = StringField('Name', validators=[DataRequired(message='Please input your name')])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phonenumber = StringField("Phone Number",
                              validators=[regexp("^[689]\d{7}$", message="Please enter a valid phone number")])
    reason = SelectField('Reason', validators=[DataRequired()],
                        choices=[('', 'Select'), ('General Inquiry', 'General Inquiry'), ('Complaint', 'Complaint'),
                                 ('Feedback', 'Feedback'), ], default='')
    message = TextAreaField('Explain your Problem', validators=[DataRequired(), Length(min=1, max=1024,
                                                                                       message="Please leave a message within 1024 characters")])
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


class EditProfileForm(Form):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Save')

    def __init__(self, user_id, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
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


# Shipping Form
class addAddressForm(Form):
    name = StringField("Address Nickname", [
        validators.Length(1, 64, message="Nickname must be between 1 to 64 characters"),
        validators.DataRequired(message="Please enter a nickname")
    ])
    location = StringField("Location", [
        validators.Length(8, 256, message="Location must be between 16 to 256 characters"),
        validators.DataRequired(message="Please enter a location")
    ])
    submit = SubmitField("Add Address")

    def validate_location(self, location):
        g = geocoder.arcgis(self.location.data)
        if not g.ok:
            raise ValidationError('This Location Does Not Exist')


class editAddressForm(Form):
    name = StringField("Address Nickname", [
        validators.Length(1, 64, message="Nickname must be between 1 to 64 characters"),
        validators.DataRequired(message="Please enter a nickname")
    ])
    location = StringField("Location", [
        validators.Length(8, 256, message="Location must be between 16 to 256 characters"),
        validators.DataRequired(message="Please enter a location")
    ])
    submit = SubmitField("Save")

    def validate_location(self, location):
        g = geocoder.osm(self.location.data)
        if not g.ok:
            raise ValidationError('This Location Does Not Exist')


class quantityForm(Form):
    quantity = IntegerField('Quantity', validators=[DataRequired(message="Quantity needs to be a number.")])
    submit = SubmitField("Add To Cart")


class addCouponForm(Form):
    name = StringField('Coupon title', validators=[DataRequired()])
    price = IntegerField('Points needed', validators=[DataRequired(message="Points needs to be a number.")])
    effect = IntegerField('Percentage', validators=[DataRequired(message='Percentage needs to be a number.')])
    submit = SubmitField("Add Coupon")


class editCouponForm(Form):
    name = StringField('Coupon title', validators=[DataRequired()])
    price = IntegerField('Points needed', validators=[DataRequired(message="Points needs to be a number.")])
    effect = IntegerField('Percentage', validators=[DataRequired(message='Percentage needs to be a number.')])
    submit = SubmitField("Save")


# Sort Functions
class SortUserForm(Form):
    sort = SelectField('Sort By', choices=[('', 'Select'), ('Ascending', 'Ascending'), ('Descending', 'Descending')],
                       default='')
    submit = SubmitField('Update')


class SortProductForm(Form):
    sort = SelectField('Filter By', validators=[DataRequired()],
                       choices=[('', 'Select'), ('Price', 'Price'), ('Quantity', 'Quantity')])
    direction = SelectField('Sort By', validators=[DataRequired()],
                            choices=[('', 'Select'), ('Ascending', 'Ascending'), ('Descending', 'Descending')],
                            default='')
    submit = SubmitField('Update')


class SortCouponForm(Form):
    sort = SelectField('Filter By', validators=[DataRequired()],
                       choices=[('', 'Select'), ('Price', 'Price'), ('Effect', 'Effect')])
    direction = SelectField('Sort By', validators=[DataRequired()],
                            choices=[('', 'Select'), ('Ascending', 'Ascending'), ('Descending', 'Descending')],
                            default='')
    submit = SubmitField('Update')


class ApplyCouponForm(Form):
    coupons = SelectField('Coupons')
    submit = SubmitField('Apply')
