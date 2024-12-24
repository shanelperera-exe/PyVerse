from selenium import webdriver
from selenium.webdriver.common.by import By
import time

GAME_TIME_LIMIT = 5  # in minutes
UPGRADES_INTERVAL = 5  # in seconds

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get(url="https://orteil.dashnet.org/experiments/cookie/")

cookie = driver.find_element(By.ID, value="cookie")

def main():
    start_time = time.time()
    last_upgrade_time = start_time
    while True:
        cookie.click()
        current_time = time.time()
        if current_time - last_upgrade_time >= UPGRADES_INTERVAL:
            choose_upgrade()
            last_upgrade_time = current_time
        if current_time - start_time > (GAME_TIME_LIMIT * 60):
            break

    cookies_per_sec = driver.find_element(By.ID, value="cps").text
    print(cookies_per_sec)
    driver.close()

def choose_upgrade():
    try:
        current_cookies = driver.find_element(By.ID, value="money").text.replace(",", "")
        current_cookies = int(current_cookies) if current_cookies.isdigit() else 0

        upgrades = get_upgrade_data()
        available_upgrades = [upgrade for upgrade in upgrades if upgrade["Price"] <= current_cookies]

        if not available_upgrades:
            return

        highest_price = available_upgrades[0]["Price"]
        best_upgrade = available_upgrades[0]["Upgrade"]
        for upgrade in available_upgrades:
            if upgrade["Price"] > highest_price:
                highest_price = upgrade["Price"]
                best_upgrade = upgrade["Upgrade"]

        upgrade_choice = driver.find_element(By.ID, value=f"buy{best_upgrade}")
        upgrade_choice.click()
    except IndexError:
        return

def get_upgrade_data():
    upgrade_names = []
    prices = []
    upgrade_store = driver.find_elements(By.CSS_SELECTOR, value="#rightPanel div div b")
    upgrade_store.pop()
    for upgrade in upgrade_store:
        item = upgrade.text.split(" - ")
        upgrade_names.append(item[0])
        prices.append(int(item[1].replace(",", "")))
    upgrades = [{"Upgrade": upgrade, "Price": price} for (upgrade, price) in zip(upgrade_names, prices)]
    return upgrades

if __name__ == "__main__":
    main()
