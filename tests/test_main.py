# Eric Olson (c) 2015
# This is a testing suit for the Capstone Team C BPA Project
# make sure a superuser is created with:
# username 'test'
#  email 'test@test.com
#  password 'password123'
# The command should look something similiar to 
# 'python manage.py createsuperuser' 
# or '$python django-admin.py createsuperuser'
# It might vary depending on your build. 

import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class TestWebsite(unittest.TestCase):
    # connects to the local server
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.get("http://127.0.0.1:8000/")

    # check to see if user can successfully login
    def test_login_page(self):
        self.driver.find_element_by_id("id_username").send_keys("test")
        self.driver.find_element_by_id("id_password").send_keys("password123")
        # This works, but may need to be fixed later on. Basically clicks on the
        # login button, as it's the first button to be found.
        self.driver.find_element_by_class_name("button").click()
        assert "Dashboard" in self.driver.title

    # tests to see if the user can log in, then log out
    def test_logout(self):
        self.driver.find_element_by_id("id_username").send_keys("test")
        self.driver.find_element_by_id("id_password").send_keys("password123")
        # This works, but may need to be fixed later on. Basically clicks on the
        # login button, as it's the first button to be found.
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
