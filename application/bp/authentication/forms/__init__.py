from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from application.database import User


class RegistrationForm(FlaskForm):
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
        print(f"\n=== Validating Email ===")
        print(f"Checking email: {field.data}")
        user = User.query.filter_by(email=field.data).first()
        print(f"Found user: {user}")
        if user:
            print("Email already exists - raising ValidationError")
            raise ValidationError('That email is already registered.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                       validators=[DataRequired(), 
                                 Email()])
    password = PasswordField('Password', 
                           validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

