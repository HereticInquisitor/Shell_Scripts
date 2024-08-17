from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import random
import string

def generate_random_email():
    domains = ["example.com", "test.com", "demo.com"]
    letters = string.ascii_lowercase
    name = ''.join(random.choice(letters) for i in range(7))
    domain = random.choice(domains)
    return f"{name}@{domain}"

def generate_random_text():
    words = ["Sumit", "Dey", "chutiya", "hai", "Bengali", "Bhalo", "Chele", "BokaChoda", "Baal"]
    return ' '.join(random.choices(words, k=10))

def main():
    chrome_driver_path = '/home/ayush/Ayush/projects/Shell_Scripts/chromedriver'
    url = "https://sumit-dey-portfolio.vercel.app"  

    chrome_options = Options()
    chrome_options.add_argument("--headless")  
    chrome_options.add_argument("--disable-gpu")  
    chrome_options.add_argument("--window-size=1920x1080")  
    service = Service(chrome_driver_path)
    
    while True:
        driver = webdriver.Chrome(service=service, options=chrome_options)

        try:
            driver.get(url)
            time.sleep(2) 

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  

            email_input = driver.find_element(By.NAME, "senderEmail") 
            message_input = driver.find_element(By.NAME, "message")  

            random_email = generate_random_email()
            random_message = generate_random_text()

            email_input.send_keys(random_email)
            message_input.send_keys(random_message)

            send_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit'].group.flex.items-center.justify-center")
            send_button.click()

            print(f"Submitted form with email: {random_email} and message: {random_message}")

            time.sleep(5)  
        finally:
            driver.quit()

if __name__ == "__main__":
    main()
