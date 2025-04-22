from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.fields import *


class RegisterForm(FlaskForm):
    email = EmailField(label="Email Address",
                       validators=[validators.DataRequired()],
                       description="You need to signup with an email"
                       )

    password = PasswordField(label="Create Your Password",
                             validators=[
                                 validators.DataRequired(),
                             ])

    confirm = PasswordField(label="Confirm Your Password",
                            validators=[
                                validators.DataRequired(),
                                validators.EqualTo("password")
                            ]
                            )

    submit = SubmitField()

    pass

