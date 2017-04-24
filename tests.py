# tests.py

import unittest, os, time, re
from flask import abort, url_for
from flask_testing import TestCase

from app import create_app, db
from app.models import Employee, Payroll, Compensation

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException

class TestBase(TestCase):

    def create_app(self):

        # pass in test configurations
        config_name = 'testing'
        app = create_app(config_name)
        app.config.update(
            SQLALCHEMY_DATABASE_URI='mysql://esss_admin:esss2017@localhost/esss_test'
        )
        return app

    def setUp(self):
        """
        Will be called before every test
        """

        db.create_all()

        # create test admin user
        admin = Employee(id=1, password="admin", is_admin=True)

        # create test non-admin user
        employee = Employee(id=1111, password="test")

        # save users to database
        db.session.add(admin)
        db.session.add(employee)
        db.session.commit()

    def tearDown(self):
        """
        Will be called after every test
        """

        db.session.remove()
        db.drop_all()

class TestModels(TestBase):

    def test_employee_model(self):
        """
        Test number of records in Employee table
        """
        self.assertEqual(Employee.query.count(), 2)

    def test_payroll_model(self):
        """
        Test number of records in Payroll table
        """

        # create test department
        payroll = Payroll(account_type="Savings", account_num="123456789", routing_num="123456789", eid=1111)

        # save payroll to database
        db.session.add(payroll)
        db.session.commit()

        self.assertEqual(Payroll.query.count(), 1)

    def test_compensation_model(self):
        """
        Test number of records in Compensation table
        """

        # create test compensation
        compensation = Compensation(start_date="2017-01-01", end_date="2017-01-15", eid="1111", )

        # save compensation to database
        db.session.add(compensation)
        db.session.commit()

        self.assertEqual(Compensation.query.count(), 1)


class TestViews(TestBase):


    def test_homepage_view(self):
        """
        Test that homepage is accessible without login
        """
        response = self.client.get(url_for('home.homepage'))
        self.assertEqual(response.status_code, 200)

    def test_login_view(self):
        """
        Test that login page is accessible without login
        """
        response = self.client.get(url_for('auth.login'))
        self.assertEqual(response.status_code, 200)

    def test_logout_view(self):
        """
        Test that logout link is inaccessible without login
        and redirects to login page then to logout
        """
        target_url = url_for('auth.logout')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_dashboard_view(self):
        """
        Test that dashboard is inaccessible without login
        and redirects to login page then to dashboard
        """
        target_url = url_for('home.dashboard')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_admin_dashboard_view(self):
        """
        Test that dashboard is inaccessible without login
        and redirects to login page then to dashboard
        """
        target_url = url_for('home.admin_dashboard')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_personalinfos_view(self):
        """
        Test that personalinfos page is inaccessible without login
        and redirects to login page then to payrolls page
        """
        target_url = url_for('admin.list_personalinfos')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_payrolls_view(self):
        """
        Test that payrolls page is inaccessible without login
        and redirects to login page then to roles page
        """
        target_url = url_for('admin.list_payrolls')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_compensations_view(self):
        """
        Test that compensations page is inaccessible without login
        and redirects to login page then to employees page
        """
        target_url = url_for('admin.select_employee')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)


class TestErrorPages(TestBase):

    def test_403_forbidden(self):
        # create route to abort the request with the 403 Error
        @self.app.route('/403')
        def forbidden_error():
            abort(403)

        response = self.client.get('/403')
        self.assertEqual(response.status_code, 403)
        self.assertTrue("403 Error" in response.data)

    def test_404_not_found(self):
        response = self.client.get('/nothinghere')
        self.assertEqual(response.status_code, 404)
        self.assertTrue("404 Error" in response.data)

    def test_500_internal_server_error(self):
        # create route to abort the request with the 500 Error
        @self.app.route('/500')
        def internal_server_error():
            abort(500)

        response = self.client.get('/500')
        self.assertEqual(response.status_code, 500)
        self.assertTrue("500 Error" in response.data)
    

class Logintest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://127.0.0.1:5000/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    """
    Test that admin is able to login successfully to admin dashboard
    """
    def test_login(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_link_text("Login").click()
        driver.find_element_by_id("id").clear()
        driver.find_element_by_id("id").send_keys("1")
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("admin")
        driver.find_element_by_id("submit").click()
        driver.find_element_by_link_text("Logout").click()
   
    """
    Test unsuccessful login due to wrong credentials
    """
    def test_unsuccessfullogin(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_link_text("Login").click()
        driver.find_element_by_id("id").clear()
        driver.find_element_by_id("id").send_keys("1")
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("123")
        driver.find_element_by_id("submit").click()
    
    """
    Test successful admin editing of employee's personal info
    """
    def test_successful_admin_edit_personalinfo(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_link_text("Login").click()
        driver.find_element_by_id("id").clear()
        driver.find_element_by_id("id").send_keys("1")
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("admin")
        driver.find_element_by_id("submit").click()
        driver.find_element_by_link_text("Personal Info").click()
        driver.find_element_by_xpath("//a[contains(@href, '/admin/personalinfos/edit/1111')]").click()
        driver.find_element_by_id("city").clear()
        driver.find_element_by_id("city").send_keys("Austin")
        driver.find_element_by_id("zip").clear()
        driver.find_element_by_id("zip").send_keys("78759")
        driver.find_element_by_id("email").clear()
        driver.find_element_by_id("email").send_keys("test1@test.com")
        driver.find_element_by_id("first_name").clear()
        driver.find_element_by_id("first_name").send_keys("test")
        driver.find_element_by_id("last_name").clear()
        driver.find_element_by_id("last_name").send_keys("test")
        driver.find_element_by_id("middle_name").clear()
        driver.find_element_by_id("middle_name").send_keys("test")
        driver.find_element_by_id("dob").clear()
        driver.find_element_by_id("dob").send_keys("1988-03-08")
        driver.find_element_by_id("home_phone").clear()
        driver.find_element_by_id("home_phone").send_keys("2815500012")
        driver.find_element_by_id("cell_phone").clear()
        driver.find_element_by_id("cell_phone").send_keys("2811234568")
        driver.find_element_by_id("submit").click()
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == '__main__':
    unittest.main()