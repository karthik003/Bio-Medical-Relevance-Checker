from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired,Email,EqualTo
from wtforms import ValidationError

class SearchForm(FlaskForm):
    userid=StringField('User-ID')
    search=StringField('Query',validators=[DataRequired()])
    submit=SubmitField('Search')
    

class LoginForm(FlaskForm):
    email=StringField('Email',validators=[DataRequired(),Email()])
    password=StringField('Password',validators=[DataRequired()])
    submit=SubmitField('Login')

class RegistrationForm(FlaskForm):
    email=StringField('Email',validators=[DataRequired(),Email()])
    username=StringField('Username',validators=[DataRequired()])
    password=PasswordField('Password',validators=[DataRequired(),EqualTo('conf_password',message='Passwords must match')])
    conf_password=PasswordField('Confirm Password',validators=[DataRequired()])
    submit= SubmitField('Register')

    def check_email(self,field): 
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Your Email has already been registered!')

    def check_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username has been taken!')