# app/admin/views.py

from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import admin
from forms import PersonalInfoForm, PayrollForm, CompensationForm, RegistrationForm
from .. import db
from ..models import Employee, Payroll, Compensation


def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.is_admin:
        abort(403)



@admin.route('/addemployee', methods=['GET', 'POST'])
def add_employee():
    """
    Handle requests to the /addemployee route
    Add an employee to the database through the registration form
    """

    check_admin()
    
    form = RegistrationForm()
    if form.validate_on_submit():
        employee = Employee(email=form.email.data,
                            id=form.id.data,
                            dob=form.dob.data,
                            first_name=form.first_name.data,
                            last_name=form.last_name.data,
                            password=form.password.data,
                            middle_name=form.middle_name.data,
                            street=form.street.data,
                            city=form.city.data,
                            zip=form.zip.data,
                            state=form.state.data,
                            home_phone=form.home_phone.data,
                            cell_phone=form.cell_phone.data)

        # add employee to the database
        db.session.add(employee)
        db.session.commit()
        flash('You have successfully registered! You may now login.')

        # redirect to the login page
        return redirect(url_for('home.dashboard'))

    # load registration template
    return render_template('admin/register.html', form=form, title='Register')



#############################################
# Personal Info Views
#############################################

@admin.route('/personalinfos', methods=['GET', 'POST'])
@login_required
def list_personalinfos():
    """
    List personal info for all employees
    """
    check_admin()

    personalinfos = Employee.query.all()

    return render_template('admin/personalinfos/personalinfos.html',
                           personalinfos=personalinfos, title="Personal Infos")


@admin.route('/personalinfos/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_personalinfo(id):
    """
    Edit an employee's personal info
    """
    check_admin()

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
        return redirect(url_for('admin.list_personalinfos'))

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

    return render_template('admin/personalinfos/personalinfo.html', action="Edit",
                           form=form,
                           personalinfo=personalinfo, title="Edit Personal Info")

###########################################
# Payroll Views
###########################################

@admin.route('/payrolls')
@login_required
def list_payrolls():
    check_admin()
    """
    List payroll info for all employees
    """
    payrolls = Payroll.query.all()
    return render_template('admin/payrolls/payrolls.html',
                           payrolls=payrolls, title='Payrolls')


@admin.route('/payrolls/add', methods=['GET', 'POST'])
@login_required
def add_payroll():
    """
    Add payroll info to the database
    """
    check_admin()


    add_payroll = True

    form = PayrollForm()
    if form.validate_on_submit(): 
        payroll = Payroll(account_type=form.account_type.data,
                          account_num=form.account_num.data,
                          routing_num=form.routing_num.data,
                          amount_withheld=form.amount_withheld.data,
                          num_allowances=form.num_allowances.data,
                          claim_exemption=form.claim_exemption.data,
                          eid=form.eid.data)

        if Payroll.query.filter_by(eid=form.eid.data).first():
            flash('ERROR: Payroll info has already been entered for this employee.')
    
        
        else:
            db.session.add(payroll)
            db.session.commit()
            flash('You have successfully added new payroll info.')
        # redirect to the payrolls page
        return redirect(url_for('admin.list_payrolls'))
        
    return render_template('admin/payrolls/payroll.html', add_payroll=add_payroll,
                       form=form, title='Add Payroll')


@admin.route('/payrolls/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_payroll(id):
    """
    Edit payroll info for an employee
    """
    check_admin()

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
        return redirect(url_for('admin.list_payrolls'))

    form.account_type.data = payroll.account_type
    form.account_num.data = payroll.account_num
    form.routing_num.data = payroll.routing_num
    form.amount_withheld.data = payroll.amount_withheld
    form.num_allowances.data = payroll.num_allowances
    form.claim_exemption.data = payroll.claim_exemption
    return render_template('admin/payrolls/payroll.html', add_payroll=add_payroll,
                           form=form, title="Edit Payroll")


@admin.route('/payrolls/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_payroll(id):
    """
    Delete an employee's payroll info from the database
    """
    check_admin()

    payroll = Payroll.query.get_or_404(id)
    db.session.delete(payroll)
    db.session.commit()
    flash('You have successfully deleted the payroll info.')

    # redirect to the roles page
    return redirect(url_for('admin.list_payrolls'))

    return render_template(title="Delete Payroll")

    
##############################################
    # Compensation Views
##############################################

@admin.route('/compensations/selectemployee', methods=['GET', 'POST'])
@login_required
def select_employee():
    """
    Select employee to view Compensation
    """
    check_admin()

    employees = Employee.query.all()

    return render_template('admin/compensations/selectemployee.html',
                           employees=employees, title="Select Employee")



@admin.route('/compensations/list/<int:id>', methods=['GET', 'POST'])
@login_required
def list_compensations(id):
    check_admin()
    """
    List compensation info for all employees
    """
    compensations = Compensation.query.filter_by(eid=id).all()
    return render_template('admin/compensations/compensations.html',
                           compensations=compensations, title='Compensations')


@admin.route('/compensations/add', methods=['GET', 'POST'])
@login_required
def add_compensation():
    """
    Add compensation info to the database
    """
    check_admin()

    add_compensation = True

    form = CompensationForm()
    if form.validate_on_submit(): 
        compensation = Compensation(start_date=form.start_date.data,
                          end_date=form.end_date.data,
                          net_pay=form.net_pay.data,
                          gross_pay=form.gross_pay.data,
                          hourly_wage=form.hourly_wage.data,
                          hours_worked=form.hours_worked.data,
                         eid=form.eid.data)
                          
        db.session.add(compensation)
        db.session.commit()
        flash('You have successfully added new compensation info.')
        # redirect to the compensations page
        return redirect(url_for('admin.list_compensations'))
        
    return render_template('admin/compensations/compensation.html', add_compensation=add_compensation,
                       form=form, title='Add Compensation')


@admin.route('/compensations/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_compensation(id):
    """
    Edit compensation info for an employee
    """
    check_admin()

    add_compensation = False

    compensation = Compensation.query.get_or_404(id)
    form = CompensationForm(obj=compensation)
    if form.validate_on_submit():
        compensation.start_date = form.start_date.data
        compensation.end_date = form.end_date.data
        compensation.net_pay = form.net_pay.data
        compensation.gross_pay = form.gross_pay.data
        compensation.hourly_wage = form.hourly_wage.data
        compensation.hours_worked = form.hours_worked.data
        db.session.add(compensation)
        db.session.commit()
        flash('You have successfully edited the compensation info.')

        # redirect to the compensations page
        return redirect(url_for('admin.list_compensations'))

    form.start_date.data = compensation.start_date
    form.end_date.data = compensation.end_date
    form.net_pay.data = compensation.net_pay
    form.gross_pay.data = compensation.gross_pay
    form.hourly_wage.data = compensation.hourly_wage
    form.hours_worked.data = compensation.hours_worked
    
    return render_template('admin/compensations/compensation.html', add_compensation=add_compensation,
                           form=form, title="Edit Compensation")


@admin.route('/compensations/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_compensation(id):
    """
    Delete an employee's compensation info from the database
    """
    check_admin()

    compensation = Compensation.query.get_or_404(id)
    db.session.delete(compensation)
    db.session.commit()
    flash('You have successfully deleted the compensation info.')

    # redirect to the compensations page
    return redirect(url_for('admin.list_compensations'))

    return render_template(title="Delete compensation")
