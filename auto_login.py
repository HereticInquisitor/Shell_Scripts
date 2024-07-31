# Make sure Chrome is installed 
# Install stable version of Chrome-driver from here -->https://googlechromelabs.github.io/chrome-for-testing/
# unzip the folder and take out the chromedriver file
# paste the path of thr chrome-driver file in the executable path
# pip install selenium
from selenium import webdriver

username="2021itb016.ayush@students.iiests.ac.in"
password="1nIrel@nd"

url="https://authentication.iiests.ac.in:8003/index.php?zone=hostelnetworks&redirurl=http%3A%2F%2Fdetectportal.brave-http-only.com%2F"

service= webdriver.ChromeService(executable_path="/home/ayush/Ayush/projects/Shell_Scripts/chromedriver")
driver= webdriver.Chrome(service=service)

driver.get(url)
driver.find_element("auth_user").send_keys(username)
driver.find_element("auth_pass").send_keys(password)
driver.find_element_by_css_selector("input[type=\"checkbox\" i]").click()
driver.find_element_by_css_selector("input[type=\"submit\" i]").click()


