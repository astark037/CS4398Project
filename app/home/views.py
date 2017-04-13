# app/home/views.py

from flask import flash, abort, render_template, redirect, url_for
from flask_login import current_user, login_required

from . import home
from forms import PersonalInfoForm, PayrollForm, CompensationForm
from .. import db
from ..models import Employee, Payroll, Compensation

@home.route('/')
def homepage():
    """
    Render the homepage template on the / route
    """
    return render_template('home/index.html', title="Welcome")

@home.route('/dashboard')
@login_required
def dashboard():
    """
    Render the dashboard template on the /dashboard route
    """
    return render_template('home/dashboard.html', title="Dashboard")

@home.route('/personalinfos/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_personalinfo(id):
    """
    Edit an employee's personal info
    """

    personalinfo = Employee.query.get_or_404(id)
    form = PersonalInfoForm(obj=personalinfo)
    if form.validate_on_submit():
        personalinfo.first_name = form.first_name.data
        personalinfo.last_name = form.last_name.data
        personalinfo.middle_name = form.middle_name.data
        personalinfo.dob = form.dob.data
        personalinfo.email = form.email.data
        personalinfo.street = form.street.data
        personalinfo.city = form.city.data
        personalinfo.zip = form.zip.data
        personalinfo.state = form.state.data
        personalinfo.home_phone = form.home_phone.data
        personalinfo.cell_phone = form.cell_phone.data

        db.session.commit()
        flash('You have successfully edited the employee.')

        # redirect to the employee page
        return redirect(url_for('home.dashboard'))

    form.first_name.data = personalinfo.first_name
    form.last_name.data = personalinfo.last_name
    form.middle_name.data = personalinfo.middle_name
    form.dob.data = personalinfo.dob
    form.email.data = personalinfo.email
    form.street.data = personalinfo.street
    form.city.data = personalinfo.city
    form.zip.data = personalinfo.zip
    form.state.data = personalinfo.state
    form.home_phone.data = personalinfo.home_phone
    form.cell_phone.data = personalinfo.cell_phone

    return render_template('home/personalinfo.html', action="Edit",
                           form=form,
                           personalinfo=personalinfo, title="Edit Personal Info")


@home.route('/payrolls')
@login_required
def list_payrolls():
    """
    List payroll info for this employee
    """
    payrolls = Payroll.query.filter_by(eid=current_user.id).all()
    return render_template('home/payrolls.html',
                           payrolls=payrolls, title='Payrolls')




@home.route('/payrolls/add', methods=['GET', 'POST'])
@login_required
def add_payroll():
    """
    Add payroll info to the database
    """


    add_payroll = True

    form = PayrollForm()
    if form.validate_on_submit(): 
        payroll = Payroll(account_type=form.account_type.data,
                          account_num=form.account_num.data,
                          routing_num=form.routing_num.data,
                          amount_withheld=form.amount_withheld.data,
                          num_allowances=form.num_allowances.data,
                          claim_exemption=form.claim_exemption.data,
                         eid=current_user.id)
                          
        db.session.add(payroll)
        db.session.commit()
        flash('You have successfully added new payroll info.')
        # redirect to the payrolls page
        return redirect(url_for('home.dashboard'))
        
    return render_template('home/payroll.html', add_payroll=add_payroll,
                       form=form, title='Add Payroll')


@home.route('/payrolls/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_payroll(id):
    """
    Edit payroll info for an employee
    """

    add_payroll = False

    payroll = Payroll.query.get_or_404(id)
    form = PayrollForm(obj=payroll)
    if form.validate_on_submit():
        payroll.account_type = form.account_type.data
        payroll.account_num = form.account_num.data
        payroll.routing_num = form.routing_num.data
        payroll.amount_withheld = form.amount_withheld.data
        payroll.num_allowances = form.num_allowances.data
        payroll.claim_exemption = form.claim_exemption.data
        db.session.add(payroll)
        db.session.commit()
        flash('You have successfully edited the payroll info.')

        # redirect to the payrolls page
        return redirect(url_for('home.dashboard'))

    form.account_type.data = payroll.account_type
    form.account_num.data = payroll.account_num
    form.routing_num.data = payroll.routing_num
    form.amount_withheld.data = payroll.amount_withheld
    form.num_allowances.data = payroll.num_allowances
    form.claim_exemption.data = payroll.claim_exemption
    return render_template('home/payroll.html', add_payroll=add_payroll,
                           form=form, title="Edit Payroll")


@home.route('/compensations')
@login_required
def list_compensations():
    """
    List compensation info for all employees
    """
    compensations = Compensation.query.filter_by(eid=current_user.id).all()
    return render_template('home/compensations.html',
                           compensations=compensations, title='Compensations')


@home.route('/admin/dashboard')
@login_required
def admin_dashboard():
    # prevent non-admins from accessing the page
    if not current_user.is_admin:
        abort(403)

    return render_template('home/admin_dashboard.html', title="Dashboard")
