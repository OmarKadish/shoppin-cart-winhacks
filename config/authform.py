from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError
from wtforms.validators import Length,EqualTo,Email,DataRequired 
from .models import User

class RegisterForm(FlaskForm):
    name = StringField(label = 'User Name:', validators = [Length(min = 2,max = 30), DataRequired()])
    email = StringField(label = 'Email Address:', validators = [Email(), DataRequired()])
    password = PasswordField(label = 'Password:', validators = [Length(min = 6), DataRequired()])
    balance = StringField(label = 'Balance:', validators=[Length(min = 2, max = 30), DataRequired()])
    submit = SubmitField(label = 'Create Account')

    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError('Hey! This email is taken. Please change the email!')
        
class LoginForm(FlaskForm):
    email = StringField(label = 'Email', validators=[DataRequired(), Email()])
    password = PasswordField(label = 'Password', validators=[DataRequired()])
    submit = SubmitField(label = 'Login')