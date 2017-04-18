# app/home/forms.py

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError, IntegerField, BooleanField, DecimalField, SelectField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange, AnyOf
from ..models import Employee, Payroll, Compensation

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
    state = SelectField('State', choices = [('AL', 'AL'), ('AK', 'AK'), ('AZ', 'AZ'), ('AR', 'AR'), 
                                            ('CA', 'CA'), ('CO', 'CO'), ('CT', 'CT'), ('DE', 'DE'), 
                                            ('FL', 'FL'), ('GA', 'GA'), ('HI', 'HI'), ('ID', 'ID'), 
                                            ('IL', 'IL'), ('IN', 'IN'), ('IA', 'IA'), ('KS', 'KS'), 
                                            ('KY', 'KY'), ('LA', 'LA'), ('ME', 'ME'), ('MD', 'MD'), 
                                            ('MA', 'MA'), ('MI', 'MI'), ('MN', 'MN'), ('MS', 'MS'), 
                                            ('MO', 'MO'), ('MT', 'MT'), ('NE', 'NE'), ('NV', 'NV'), ('NH', 'NH'),
                                            ('NJ', 'NJ'), ('NM', 'NM'), ('NY', 'NY'),
                                            ('NC', 'NC'), ('ND', 'ND'), ('OH', 'OH'), ('OK', 'OK'), 
                                            ('OR', 'OR'), ('PA', 'PA'), ('RI', 'RI'), ('SC', 'SC'), 
                                            ('SD', 'SD'), ('TN', 'TN'), ('TX', 'TX'), ('UT', 'UT'), 
                                            ('VT', 'VT'), ('VA', 'VA'), ('WA', 'WA'), ('WV', 'WV'), 
                                            ('WI', 'WI'), ('WY', 'WY')])
    home_phone = IntegerField('Home Phone')
    cell_phone = IntegerField('Cell Phone', validators=[DataRequired()])
    submit = SubmitField('Submit')

class PayrollForm(FlaskForm):
    """
    Form for admin to edit employee personal info
    """
    #eid = StringField('Employee ID', validators=[DataRequired(), ])
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
        if Payroll.query.filter_by(eid=field.data).first():
            raise ValidationError('Payroll info has already been entered for this employee.')

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
