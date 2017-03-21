# app/auth/forms.py

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo, Length, AnyOf

from ..models import Employee

class RegistrationForm(FlaskForm):
    """
    Form for users to create new account
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    id = StringField('Employee ID', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=1, max=60)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=1, max=60)])
    middle_name = StringField('Middle Name', validators=[Length(min=1, max=60)])
    home_address = StringField('Home Address', validators=[DataRequired(), Length(max=60)])
    mailing_address = StringField('Mailing Address', validators=[DataRequired(), Length(max=60)])
    home_phone = StringField('Home Phone', validators=[Length(max=15)])
    cell_phone = StringField('Cell Phone', validators=[DataRequired(), Length(max=15)])

    password = PasswordField('Password', validators=[
                                        DataRequired(),
                                        EqualTo('confirm_password')
                                        ])
    confirm_password = PasswordField('Confirm Password')
    submit = SubmitField('Register')

    def validate_email(self, field):
        if Employee.query.filter_by(email=field.data).first():
            raise ValidationError('Email is already in use.')

    def validate_emp_id(self, field):
        if Employee.query.filter_by(id=field.data).first():
            raise ValidationError('Employee ID is already in use.')

class LoginForm(FlaskForm):
    """
    Form for users to login
    """
    id = StringField('Employee ID', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')