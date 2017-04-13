# app/admin/forms.py

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError, IntegerField, BooleanField, DecimalField, SelectField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange, AnyOf
from ..models import Employee, Payroll, Compensation


class RegistrationForm(FlaskForm):
    """
    Form for users to create new account
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    id = StringField('Employee ID', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=1, max=60)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=1, max=60)])
    middle_name = StringField('Middle Name', validators=[Length(min=1, max=60)])
    dob = DateField('Date of Birth (format: YYYY-MM-DD)', validators=[DataRequired()], format='%Y-%m-%d')
    street = StringField('Street', validators=[DataRequired(), Length(max=60)])
    city = StringField('City', validators=[DataRequired(), Length(max=60)])
    zip = IntegerField('ZIP', validators=[DataRequired(), NumberRange(min=1000, max=99999)])
    state = SelectField('State', choices = [('Alabama', 'AL'), ('Alaska', 'AK'), ('Arizona', 'AZ'), ('Arkansas', 'AR'), 
                                            ('California', 'CA'), ('Colorado', 'CO'), ('Connecticut', 'CT'), ('Delaware', 'DE'), 
                                            ('Florida', 'FL'), ('Georgia', 'GA'), ('Hawaii', 'HI'), ('Idaho', 'ID'), 
                                            ('Illinois', 'IL'), ('Indiana', 'IN'), ('Iowa', 'IA'), ('Kansas', 'KS'), 
                                            ('Kentucky', 'KY'), ('Louisian', 'LA'), ('Maine', 'ME'), ('Maryland', 'MD'), 
                                            ('Massachusetts', 'MA'), ('Michigan', 'MI'), ('Minnesota', 'MN'), ('Mississippi', 'MS'), 
                                            ('Missouri', 'MO'), ('Montana', 'MT'), ('Nebraska', 'NE'), ('Nevada', 'NV'), ('New Hampshire', 'NH'),
                                            ('New Jersey', 'NJ'), ('New Mexico', 'NM'), ('New York', 'NY'),
                                            ('North Carolina', 'NC'), ('North Dakota', 'ND'), ('Ohio', 'OH'), ('Oklahoma', 'OK'), 
                                            ('Oregon', 'OR'), ('Pennsylvania', 'PA'), ('Rhode Island', 'RI'), ('South Carolina', 'SC'), 
                                            ('South Dakota', 'SD'), ('Tennessee', 'TN'), ('Texas', 'TX'), ('Utah', 'UT'), 
                                            ('Vermont', 'VT'), ('Virginia', 'VA'), ('Washington', 'WA'), ('West Virginia', 'WV'), 
                                            ('Wisconsin', 'WI'), ('Wyoming', 'WY')])
    home_phone = IntegerField('Home Phone')
    cell_phone = IntegerField('Cell Phone', validators=[DataRequired()])

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



class PersonalInfoForm(FlaskForm):
    """
    Form for admin to edit employee personal info
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=1, max=60)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=1, max=60)])
    middle_name = StringField('Middle Name', validators=[Length(min=1, max=60)])
    dob = DateField('Date of Birth (format: YYYY-MM-DD)', validators=[DataRequired()], format='%Y-%m-%d')
    street = StringField('Street', validators=[DataRequired(), Length(max=60)])
    city = StringField('City', validators=[DataRequired(), Length(max=60)])
    zip = IntegerField('ZIP', validators=[DataRequired(), NumberRange(min=1000, max=99999)])
    state = SelectField('State', choices = [('Alabama', 'AL'), ('Alaska', 'AK'), ('Arizona', 'AZ'), ('Arkansas', 'AR'), 
                                            ('California', 'CA'), ('Colorado', 'CO'), ('Connecticut', 'CT'), ('Delaware', 'DE'), 
                                            ('Florida', 'FL'), ('Georgia', 'GA'), ('Hawaii', 'HI'), ('Idaho', 'ID'), 
                                            ('Illinois', 'IL'), ('Indiana', 'IN'), ('Iowa', 'IA'), ('Kansas', 'KS'), 
                                            ('Kentucky', 'KY'), ('Louisian', 'LA'), ('Maine', 'ME'), ('Maryland', 'MD'), 
                                            ('Massachusetts', 'MA'), ('Michigan', 'MI'), ('Minnesota', 'MN'), ('Mississippi', 'MS'), 
                                            ('Missouri', 'MO'), ('Montana', 'MT'), ('Nebraska', 'NE'), ('Nevada', 'NV'), ('New Hampshire', 'NH'),
                                            ('New Jersey', 'NJ'), ('New Mexico', 'NM'), ('New York', 'NY'),
                                            ('North Carolina', 'NC'), ('North Dakota', 'ND'), ('Ohio', 'OH'), ('Oklahoma', 'OK'), 
                                            ('Oregon', 'OR'), ('Pennsylvania', 'PA'), ('Rhode Island', 'RI'), ('South Carolina', 'SC'), 
                                            ('South Dakota', 'SD'), ('Tennessee', 'TN'), ('Texas', 'TX'), ('Utah', 'UT'), 
                                            ('Vermont', 'VT'), ('Virginia', 'VA'), ('Washington', 'WA'), ('West Virginia', 'WV'), 
                                            ('Wisconsin', 'WI'), ('Wyoming', 'WY')])
    home_phone = IntegerField('Home Phone')
    cell_phone = IntegerField('Cell Phone', validators=[DataRequired()])
    submit = SubmitField('Submit')



class PayrollForm(FlaskForm):
    """
    Form for admin to edit employee personal info
    """
    eid = StringField('Employee ID', validators=[DataRequired(), ])
    account_type = SelectField('Account Type', choices = [('Checking', 'Checking'), ('Savings', 'Savings')])
    account_num = StringField('Account Number', validators=[DataRequired(), Length(min=9, max=9)])
    routing_num = StringField('Routing Number', validators=[DataRequired(), Length(min=9, max=9)])
    amount_withheld = IntegerField('Amount Withheld', validators=[ NumberRange(min=0)])
    num_allowances = IntegerField('Number of Allowances', validators=[ NumberRange(min=0)])
    claim_exemption = BooleanField('Claim Exemption', validators=[], default=False)
    submit = SubmitField('Submit')
    
    def validate_eid(self, field):
        if Employee.query.filter_by(id=field.data).first() == None:
            raise ValidationError('Employee ID not found.')

class CompensationForm(FlaskForm):
    """
    Form for admin to edit employee compensation info
    """
    eid = StringField('Employee ID', validators=[DataRequired()])
    start_date = DateField('Start Date (format: YYYY-MM-DD)', validators=[DataRequired()], format='%Y-%m-%d')
    end_date = DateField('End Date (format: YYYY-MM-DD)', validators=[DataRequired()], format='%Y-%m-%d')
    net_pay = DecimalField('Net Pay', validators=[DataRequired()])
    gross_pay = DecimalField('Gross Pay', validators=[DataRequired()])
    hourly_wage = DecimalField('Hourly Wage', validators=[DataRequired()])
    hours_worked = DecimalField('Hours Worked', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_eid(self, field):
        if Employee.query.filter_by(id=field.data).first() == None:
            raise ValidationError('Employee ID not found.')
