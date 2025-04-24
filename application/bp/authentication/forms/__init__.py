"""Authentication forms module"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from application.database import User


class RegistrationForm(FlaskForm):
    """Registration form"""
    email = StringField('Email',
                       validators=[DataRequired(), 
                                 Email()])
    password = PasswordField('Password', 
                           validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                   validators=[DataRequired(), 
                                             EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, field):
        """Custom validator for email field"""
        user = User.query.filter_by(email=field.data).first()
        if user:
            raise ValidationError('That email is already registered.')


class LoginForm(FlaskForm):
    """Login form"""
    email = StringField('Email',
                       validators=[DataRequired(), 
                                 Email()])
    password = PasswordField('Password', 
                           validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

