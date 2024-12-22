from bs4 import BeautifulSoup
import requests
import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

TARGET_PRICE = 100

static_url = "https://appbrewery.github.io/instant_pot/"
live_url = "https://www.amazon.com/Alienware-RGB-Gaming-Mouse-AW510M/dp/B07V6MDXDQ/ref=sr_1_4?crid=378N1K0PMSD73&dib=eyJ2IjoiMSJ9.07ytkWLLzfGFp4Dlcka48uUNdEkkek65rqSrQVAsgi5twowSfsnw5OenRg-oVuDmh74TT1H8eczMWyS5ae5xITx6xqfko4-tLQ7AES92jjujDK9TdPLZMtrHhIVvsYg6mqPiUpHGA2YwfX7BqFrNoaWpBpvPE0PD9jZfUrjZPLmnb3WtNkfF4NL8iO5KcExqwwRhkGvhYMxaerMp31G9hWvhU5D-VR7MmIPW6qAgtX4.B8GhgxpnaD0EsryY062sTrkh-mQKI0EfGRMrGFcKuIE&dib_tag=se&keywords=alienware+mouse&qid=1734839048&sprefix=alienware+mouse%2Caps%2C362&sr=8-4"

URL = live_url

MY_EMAIL = os.environ["MY_TEST_EMAIL"]
PASSWORD = os.environ["EMAIL_SENDER_PASSWORD"]

def main():
    price, title = get_product_data()
    if price < TARGET_PRICE:
        message = f"{title} is on sale for ${price}!"
        send_email(message)

def get_product_data():
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

    response = requests.get(url=URL, headers=headers)
    response.raise_for_status()
    web_page = response.text
    soup = BeautifulSoup(web_page, "html.parser")
    price = soup.find(class_="aok-offscreen").getText()
    title = soup.find(id="productTitle").getText().strip()
    title = " ".join(title.split())
    price_without_currency = float(price.split("$")[1])
    return price_without_currency, title

def send_email(message):
    smtp_address = os.environ["MY_SMTP_ADDRESS"]
    with smtplib.SMTP(smtp_address, port=587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=os.environ["PERSONAL_EMAIL"],
            msg=f"Subject:Amazon Price Alert!\n\n{message}\n{URL}".encode("utf-8")
        )

if __name__ == "__main__":
    main()