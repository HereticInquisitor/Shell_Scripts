from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

def main():
    chrome_driver_path = '/home/ayush/Ayush/projects/Shell_Scripts/chromedriver'

    # URL to open
    url = "https://leetcode.com/problems/time-needed-to-rearrange-a-binary-string/solutions/5575807/tc-o-n-brute-force-solution-with-explanation-c-java/"

    while True:
        chrome_options = Options()

        service = Service(chrome_driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)

        try:
            driver.get(url)

            time.sleep(10)

            print("Opened page: ", driver.title)

        finally:
            driver.quit()

        time.sleep(1)

if __name__ == "__main__":
    main()
