from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, BooleanField, TextAreaField
from wtforms.fields.core import SelectField
from wtforms.validators import DataRequired, Email, Length, ValidationError, EqualTo
from flask_wtf.file import FileField
from app.models import User

class User(FlaskForm):
    username = StringField('Useranme', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, message='Password should be at least %(min)d characters long')])
    submit = SubmitField('Submit')
    
class ImageForm(FlaskForm):
    file = FileField('File Input', validators=[DataRequired()])
    image_category = [('Digital', 'Digital'),
                ('Art', 'Art'),
                ('Portrait', 'Portrait'),
                ('Random', 'Random'),
                ]
    text = StringField('Description', validators=[DataRequired()])
    categories = SelectField('Categories', choices=image_category)
    submit = SubmitField('Submit')
    
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    # def validate_username(self, username):
    #     user = User.query.filter_by(username=username.data).first()
    #     if user is not None:
    #         raise ValidationError('Please use a different username.')

    # def validate_email(self, email):
    #     user = User.query.filter_by(email=email.data).first()
    #     if user is not None:
    #         raise ValidationError('Please use a different email address.')
    

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, message='Password should be at least %(min)d characters long')])
    submit = SubmitField('Login')
    
class EditProfileForm(FlaskForm):
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')
        
