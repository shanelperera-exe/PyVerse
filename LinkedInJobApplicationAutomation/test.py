from selenium import webdriver
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
from selenium.webdriver.common.keys import Keys
import time
import os
import random
from selenium.common.exceptions import NoSuchElementException

load_dotenv()

job_search_url = "https://www.linkedin.com/jobs/search/?f_LF=f_AL&geoId=105665594&keywords=software%20engineer&location=Colombo%2C%20SriLanka&redirect=false&position=1&pageNum=0"

login_url = "https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin"

ACCOUNT_EMAIL = os.environ["LINKEDIN_EMAIL"]
ACCOUNT_PASSWORD = os.environ["LINKEDIN_PASSWORD"]
MOBILE_PHONE_NUMBER = os.environ["TEST_MOBILE_NUMBER"]

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)

driver.get(url=login_url)
time.sleep(1)

email_field = driver.find_element(by=By.ID, value="username")
email_field.send_keys(ACCOUNT_EMAIL)
time.sleep(1)

password_field = driver.find_element(by=By.ID, value="password")
password_field.send_keys(ACCOUNT_PASSWORD)
time.sleep(1)

password_field.send_keys(Keys.ENTER)

# Verification
time.sleep(15)

time.sleep(1)
driver.get(job_search_url)

all_job_listings = driver.find_elements(By.CSS_SELECTOR, value=".rjmNTMLkNvPwnJnFTCybgSFpgYGQ li strong")
for li in all_job_listings:
    print(li.text)


def abort_application():
    pass