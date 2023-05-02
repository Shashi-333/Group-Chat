from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import InputRequired, Length

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=10)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=4, max=10)])
    email = EmailField('Password', validators=[InputRequired(), Length(min=4, max=30)])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(),Length(min=4, max=10)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=4, max=30)])
    email = StringField('Email', validators=[InputRequired(),Length(min=4, max=10)])
    submit = SubmitField('Register')