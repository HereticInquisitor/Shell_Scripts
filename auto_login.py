# Make sure Chrome is installed 
# Install stable version of Chrome-driver from here -->https://googlechromelabs.github.io/chrome-for-testing/
# unzip the folder and take out the chromedriver file
# paste the path of thr chrome-driver file in the executable path
# pip install selenium

#Make a .env file to store the login credentials 

from selenium import webdriver
from dotenv import load_dotenv,find_dotenv
import os


load_dotenv(find_dotenv('.env'))

username=os.getenv("USER_NAME")
password=os.getenv("PASS")

url=os.getenv("URL")
# print(url)
service= webdriver.ChromeService(executable_path=os.getenv("CDRI"))
# print(os.getenv("CDRI"))
driver= webdriver.Chrome(service=service)

driver.get(url)
driver.find_element("auth_user").send_keys(username)
driver.find_element("auth_pass").send_keys(password)
driver.find_element_by_css_selector("input[type=\"checkbox\" i]").click()
driver.find_element_by_css_selector("input[type=\"submit\" i]").click()


