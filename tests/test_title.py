# Eric Olson (c) 2015
# GNU GPL V2.0

# This test checks to see if the Title page is accurate
from selenium import webdriver

# check to see if it works in Firefox
driver = webdriver.Firefox()
driver.get("http://127.0.0.1:8000/")

# test the title 
try:
  assert "BPA Project" in driver.title
except AssertionError as e:
  e.args +=('Failed to find BPA Project in webpage title',0)
  driver.close()
  raise

driver.close()


