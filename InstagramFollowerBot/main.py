from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
from dotenv import load_dotenv
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver import ActionChains

load_dotenv()

SIMILAR_ACCOUNT = "chefsteps"
USERNAME = os.environ["INSTAGRAM_USERNAME"]
PASSWORD = os.environ["INSTAGRAM_PASSWORD"]

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

class InstaFollower():
    def __init__(self):
        self.driver = webdriver.Chrome(options=chrome_options)

    def login(self):
        login_url = "https://www.instagram.com/accounts/login/"
        self.driver.get(url=login_url)
        username_field = self.driver.find_element(by=By.XPATH, value='//*[@id="loginForm"]/div[1]/div[1]/div/label/input')
        username_field.send_keys(USERNAME)
        time.sleep(2)
        password_field = self.driver.find_element(by=By.XPATH, value='//*[@id="loginForm"]/div[1]/div[2]/div/label/input')
        password_field.send_keys(PASSWORD)
        time.sleep(1)
        password_field.send_keys(Keys.ENTER)
        time.sleep(8)

    def find_followers(self):
        self.driver.get(url=f"https://www.instagram.com/{SIMILAR_ACCOUNT}/followers")
        time.sleep(5)
        followers = self.driver.find_element(By.PARTIAL_LINK_TEXT, value="followers")
        followers.click()
        time.sleep(2)

        scroll = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "(//div[@class='xyi19xy x1ccrb07 xtf3nb5 x1pc53ja x1lliihq x1iyjqo2 xs83m0k xz65tgg x1rife3k x1n2onr6'])[1]"))
        )
        for i in range(10):
            self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scroll)
            time.sleep(2)

    def follow(self):
        list_buttons = self.driver.find_elements(by=By.CSS_SELECTOR, value="button._acan._acap._acas._aj1-._ap30")
 
        for button in list_buttons:
            if button.text == "Follow":
                try:
                    ActionChains(self.driver).move_to_element(button).perform()
                    button.click()
                    time.sleep(2)
                except ElementClickInterceptedException:
                    cancel_button = self.driver.find_element(by=By.XPATH, value="//button[contains(text(), 'Cancel')]")
                    cancel_button.click()
                except Exception as e:
                    print(f"Error clicking the follow button: {e}")

bot = InstaFollower()
bot.login()
bot.find_followers()
bot.follow()