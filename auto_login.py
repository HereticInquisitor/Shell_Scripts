# Make sure Chrome is installed 
# Install stable version of Chrome-driver from here -->https://googlechromelabs.github.io/chrome-for-testing/
# unzip the folder and take out the chromedriver file
# paste the path of the chrome-driver file in the executable path
# pip install selenium and python-dotenv

#Make a .env file to store the login credentials 

from selenium import webdriver
from dotenv import load_dotenv,find_dotenv
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
# from webdriver_manager.chrome import ChromeDriverManager


from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService

load_dotenv(find_dotenv('.env'))

username=os.getenv("USER_NAME")
password=os.getenv("PASS")

url=os.getenv("URL")
# print(url)
service= webdriver.ChromeService(executable_path=os.getenv("CDRI"))
# print(os.getenv("CDRI"))
driver= webdriver.Chrome(service=service)

driver.get(url)

# Wait for the element to be present
try:
    username_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "auth_user"))
    )
    username_field.send_keys(username)
    print('s')
except Exception as e:
    print(f"An error occurred: {e}")

# driver.find_element(By.NAME,"auth_user").send_keys(username)
# driver.find_element(By.NAME,"auth_pass").send_keys(password)
# driver.find_element_by_css_selector("input[type=\"checkbox\" i]").click()
# driver.find_element_by_css_selector("input[type=\"submit\" i]").click()


