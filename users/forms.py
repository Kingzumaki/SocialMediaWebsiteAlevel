from flask_wtf import FlaskForm, RecaptchaField
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from flask_babel import _, lazy_gettext as _l
from flaskapp.models import User

#Class for SignUp which takes in the parameter FlaskForm
#FlaskForm is imported from flask_wtf


#This is the SignUp Class Form which allows the user to create an account on the site
class SignUp(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=3, max=20)] ) #This sets a limit which states that username cannot be longer than 20 characters and less 
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    # Confirm Password Field where end user enters the confirm password for their account 
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')]) # In order to confirm Password, password has to be equal to that of ConfirmPassword
    submit = SubmitField('Sign Up') #Submit button will have the text sign up
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first() #If username is not taken , username will be validated
        if user:
            raise ValidationError('Username is already associated with another account. Please choose a different one.') #If username chosen by user has already been chosen, this message will pop up


    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first() # If email is not already associated with an account , this email will be valid
        if user:
            raise ValidationError('Email is already associated with another account. ') #If email is already associated with an account on the site , this message will pop up

#This is a new message form which allows private messages to be sent
class NewMessage(FlaskForm):
    message = TextAreaField('Message', validators=[DataRequired()])  #Field where private message is enerred
    submit = SubmitField('Submit')

#This is the login class which allows user to sign into account via form .
class Login(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me') # This will appear in form and will
    recaptcha = RecaptchaField() # This class uses the function RecaptchaField which creates a recaptcha field where the user has to fill out in order to login.This prevents any bot accounts from being created
    submit = SubmitField('Login')

# This is the Update Account class which allow users to update their account via a fom
class UpdateAccount(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.') #If username chosen by user is already associated with an account , this message will pop up

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.') #If email is already associated with another account on the site , this message will pop up

# This is the Request Reset Password which allows the user to send an request password email to theiir email adress in order to change their password via a form
class RequestReset(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first() 
        if user is None:
            raise ValidationError('There is no account associated with this email. Sign Up') 

#This class allows the user to change the password of their current account to a new password 
class ResetPassword(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password ')

