# Bonneville Power Adminstration Front-End
# Copyright (C) 2015  Eric Olson
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
#
# make sure a superuser is created with:
#  username 'test'
#  email 'test@test.com
#  password 'password123'
# The command should look something similiar to 
# 'python manage.py createsuperuser' 
# or '$python django-admin.py createsuperuser'
# It might vary depending on your build. 
from django.contrib import admin
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class TestWebsite(unittest.TestCase):
    # connects to the local server
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.get("http://127.0.0.1:8000/")

  # check to see if user can successfully load a query results
    def test_query_result(self):
        self.driver.find_element_by_id("id_username").send_keys("test")
        self.driver.find_element_by_id("id_password").send_keys("password123")
        # This works, but may need to be fixed later on. Basically clicks on the
        # login button, as it's the first button to be found.
        self.driver.find_element_by_class_name("button").click()
        # find a query, and click on it
        ###########XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

    # check to see if user can successfully login
    def test_login_page(self):
        self.driver.find_element_by_id("id_username").send_keys("test")
        self.driver.find_element_by_id("id_password").send_keys("password123")
        self.driver.find_element_by_class_name("button").click()
        assert "Dashboard" in self.driver.title

    # tests to see if the user can log in, then log out
    def test_logout(self):
        self.driver.find_element_by_id("id_username").send_keys("test")
        self.driver.find_element_by_id("id_password").send_keys("password123")
        self.driver.find_element_by_class_name("button").click()
        self.driver.find_element_by_link_text("Logout").click()
        assert "Logged out | Django site admin" in self.driver.title

    # check if the contact us  page is there
    def test_contact_us_exists(self):
        self.driver.find_element_by_link_text("Contact Us").click()
        assert "Contact" in self.driver.title

    # check if the faq  page is there
    def test_faq_exists(self):
        self.driver.find_element_by_link_text("FAQs").click()
        assert "FAQ" in self.driver.title

    # check if the about page is there
    def test_about_exists(self):
        self.driver.find_element_by_link_text("About").click()
        assert "About" in self.driver.title

    # check to see the title is correct
    def test_title(self):
        assert "BPA Project" in self.driver.title

    # destroys the driver
    def tearDown(self):
        self.driver.close()

# End Class

# misc
if __name__ == "__main__":
    unittest.main()
