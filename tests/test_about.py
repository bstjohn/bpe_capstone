# Eric Olson (c) 2015
# GNU GPL V2.0

# This test checks to see if the About page is there
from selenium import webdriver
# from selenium.webdriver.common.keys import keys

# check to see if it works in Firefox
driver = webdriver.Firefox()
driver.get("http://127.0.0.1:8000/")

# checks if the about page is there
try:
    elmnt = driver.find_element_by_link_text("About")
    elmnt.click()
    driver.get("http://127.0.0.1:8000/info/about/")
    assert "About" in driver.title
    driver.close()
except:
    print("Failure to find 'About'")
    driver.close()
  
