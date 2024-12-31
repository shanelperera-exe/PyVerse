from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

ZILLOW_URL = "https://appbrewery.github.io/Zillow-Clone/"

# Google Sheet Link: https://docs.google.com/spreadsheets/d/1fIp7iM0OGRCRWi3dv-IYSCSP0_XmKu80PmAY8OUP72o/edit?usp=sharing

def main():
    links, prices, addresses = get_listing_data()
    enter_data_to_form(links, prices, addresses)

def get_listing_data():
    headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.9",
            "Priority": "u=0, i",
            "Sec-Ch-Ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": "\"Windows\"",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "cross-site",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    }

    response = requests.get(url=ZILLOW_URL ,headers=headers)
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

    driver = webdriver.Chrome(options=chrome_options)

    for listing in range(len(addresses)):
        driver.get(url=form_link)
        time.sleep(1)

        input_elements = driver.find_elements(by=By.CSS_SELECTOR, value=".Xb9hP input")

        address_field = input_elements[0]
        address_field.send_keys(addresses[listing])

        price_field = input_elements[1]
        price_field.send_keys(prices[listing])

        link_field = input_elements[2]
        link_field.send_keys(links[listing])

        submit_button = driver.find_element(by=By.CSS_SELECTOR, value=".lRwqcd span")
        submit_button.click()
        time.sleep(2)

    print("\nData entered successfully.")
    driver.quit()

if __name__ == "__main__":
    main()