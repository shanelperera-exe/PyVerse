from selenium import webdriver
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
from selenium.webdriver.common.keys import Keys
import time
import os
import random
from selenium.common.exceptions import NoSuchElementException

load_dotenv()

job_search_url = (
    "https://www.linkedin.com/jobs/search/?f_LF=f_AL&geoId=105665594"
    "&keywords=software%20engineer"
    "&location=Colombo%2C%20SriLanka"
    "&redirect=false&position=1&pageNum=0"
)

login_url = "https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin"

ACCOUNT_EMAIL = os.environ["LINKEDIN_EMAIL"]
ACCOUNT_PASSWORD = os.environ["LINKEDIN_PASSWORD"]
MOBILE_PHONE_NUMBER = os.environ["TEST_MOBILE_NUMBER"]

def abort_application():
    # Click Close Button
    close_button = driver.find_element(by=By.CLASS_NAME, value="artdeco-modal__dismiss")
    close_button.click()

    time.sleep(2)
    # Click Discard Button
    discard_button = driver.find_elements(by=By.CLASS_NAME, value="artdeco-modal__confirm-dialog-btn")[1]
    discard_button.click()

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)

driver.get(url=login_url)
time.sleep(1)

email_field = driver.find_element(by=By.ID, value="username")
email_field.send_keys(ACCOUNT_EMAIL)
time.sleep(2)

password_field = driver.find_element(by=By.ID, value="password")
password_field.send_keys(ACCOUNT_PASSWORD)
time.sleep(2)

password_field.send_keys(Keys.ENTER)

# CAPTCHA - Solve Puzzle Manually
input("Press Enter when you have solved the Captcha")

time.sleep(5)
driver.get(job_search_url)

all_listings = driver.find_elements(by=By.CSS_SELECTOR, value=".job-card-container--clickable")

# Apply for Jobs
for listing in all_listings:
    print("Opening Listing")
    listing.click()
    time.sleep(2)

    try:
        easy_apply = driver.find_element(By.CSS_SELECTOR, value=".jobs-apply-button--top-card button")
        easy_apply.click()
        time.sleep(1)

        phone_number = driver.find_element(By.CSS_SELECTOR, value=".ZxlCPgbyTcaHsoKicgLvkfGYSxPmVqWGqPk input")
        print(phone_number.text)
        phone_number.send_keys(MOBILE_PHONE_NUMBER)

        next_button_1 = driver.find_element(By.CSS_SELECTOR, value=".display-flex button span")
        next_button_1.click()

        next_button_2 = driver.find_elements(By.CSS_SELECTOR, value=".GZCoGHFHJZKbmGOJGPEEppeBZcZuqAMrTmwU form footer button")[1]
        next_button_2.click()

        question_inputs = driver.find_elements(By.CSS_SELECTOR, value=".GZCoGHFHJZKbmGOJGPEEppeBZcZuqAMrTmwU form input")

        for i in range(len(question_inputs)):
            question_inputs = driver.find_elements(By.CSS_SELECTOR, value=".GZCoGHFHJZKbmGOJGPEEppeBZcZuqAMrTmwU form input")
            question_input = question_inputs[i]
            
            input_type = question_input.get_attribute("type")
            print(f"Processing input type: {input_type}")
            
            if input_type == "radio":
                radio_buttons = driver.find_elements(By.CSS_SELECTOR, value=".ZxlCPgbyTcaHsoKicgLvkfGYSxPmVqWGqPk fieldset div input")
                if radio_buttons:
                    random_button = random.choice(radio_buttons)
                    driver.execute_script("arguments[0].click();", random_button)
                    print("Random radio button clicked.")
            
            elif input_type == "text":
                question_input.clear()
                random_text = str(random.randint(1, 8))
                question_input.send_keys(random_text)
                print(f"Entered text: {random_text}")
                
            elif input_type == "select-one":
                dropdown_options = question_input.find_elements(By.TAG_NAME, value="option")
                if len(dropdown_options) > 1:
                    random_option = random.choice(dropdown_options[1:])
                    random_option.click()
                    print(f"Selected dropdown option: {random_option.text}")

        review_button = driver.find_elements(By.CSS_SELECTOR, value=".display-flex button")[1]
        review_button.click()

        submit_button = driver.find_elements(By.CSS_SELECTOR, value="footer button")[1]
        submit_button.click()

    except NoSuchElementException:
        abort_application()
        print("No application button, skipped.")
        continue

time.sleep(5)
driver.quit()