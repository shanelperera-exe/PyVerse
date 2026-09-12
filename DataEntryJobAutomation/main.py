from bs4 import BeautifulSoup
import requests
import socket
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

# Force IPv4 in WSL to prevent IPv6 connection timeouts
orig_getaddrinfo = socket.getaddrinfo
def getaddrinfo_ipv4(host, port, family=0, type=0, proto=0, flags=0):
    return orig_getaddrinfo(host, port, socket.AF_INET, type, proto, flags)
socket.getaddrinfo = getaddrinfo_ipv4

ZILLOW_URL = "https://appbrewery.github.io/Zillow-Clone/"

# Google Sheet Link: https://docs.google.com/spreadsheets/d/1fIp7iM0OGRCRWi3dv-IYSCSP0_XmKu80PmAY8OUP72o/edit?usp=sharing

def main():
    print("Fetching listing data from Zillow clone...")
    links, prices, addresses = get_listing_data()
    print(f"Successfully scraped {len(links)} listings.")
    print("Launching browser to enter data into Google Form...")
    enter_data_to_form(links, prices, addresses)

def get_listing_data():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }

    response = requests.get(url=ZILLOW_URL, headers=headers)
    response.raise_for_status()
    webpage = response.text

    soup = BeautifulSoup(webpage, features='html.parser')

    listings = soup.find_all(name="li", class_="ListItem-c11n-8-84-3-StyledListCardWrapper")
    links = [listing.find(name="a").get("href") for listing in listings]

    price_data = soup.select(selector=".PropertyCardWrapper span")
    prices = [price.getText().replace("/mo", "").split("+")[0] for price in price_data]

    address_data = soup.select(selector=".StyledPropertyCardDataWrapper address")
    addresses = [" ".join(address.getText().split()).replace("|", "").replace("\n", "") for address in address_data]

    return links, prices, addresses

def enter_data_to_form(links, prices, addresses):
    form_link = "https://docs.google.com/forms/d/e/1FAIpQLScfRo1TfT3W2GFp5U7a0ZsjjKOjPb5h-shwX1s9TcT116glkg/viewform?usp=header"

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--lang=en')
    prefs = {
        "intl.accept_languages": "en,en_US",
        "translate_whitelists": {"es": "en"},
        "translate": {"enabled": "true"}
    }
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_experimental_option("detach", True)

    CHROME_BIN = "/home/shanelperera/.cache/selenium/chrome/linux64/152.0.7977.82/chrome"
    DRIVER_BIN = "/home/shanelperera/.cache/selenium/chromedriver/linux64/152.0.7977.82/chromedriver"

    if os.path.exists(CHROME_BIN):
        chrome_options.binary_location = CHROME_BIN

    service = Service(executable_path=DRIVER_BIN) if os.path.exists(DRIVER_BIN) else None
    driver = webdriver.Chrome(service=service, options=chrome_options) if service else webdriver.Chrome(options=chrome_options)

    for listing in range(len(addresses)):
        driver.get(url=form_link)
        input_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".Xb9hP input"))
        )

        print(f"  [{listing + 1}/{len(addresses)}] Submitting: {addresses[listing]} - {prices[listing]}")
        address_field = input_elements[0]
        address_field.send_keys(addresses[listing])

        price_field = input_elements[1]
        price_field.send_keys(prices[listing])

        link_field = input_elements[2]
        link_field.send_keys(links[listing])

        submit_button = driver.find_element(by=By.CSS_SELECTOR, value=".lRwqcd span")
        submit_button.click()
        time.sleep(1)

    print("\nData entered successfully!")
    driver.quit()

if __name__ == "__main__":
    main()