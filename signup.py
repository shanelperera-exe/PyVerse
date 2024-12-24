from selenium import webdriver
from selenium.webdriver.common.by import By

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

def main():
    first_name, last_name, email_address = get_details()
    print("\nForwarding to the webpage...")
    register(first_name, last_name, email_address)
    print("Signed up successfully.")

def get_details():
    print("Enter following details signup to The London App Brewery Newsletter.")
    first_name = input("Enter your first name: ").strip().title()
    last_name = input("Enter your last name: ").strip().title()
    email_address = input("Enter your email address: ").strip()
    return first_name, last_name, email_address

def register(first_name, last_name, email_address):
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url="https://secure-retreat-92358.herokuapp.com/")

    fname = driver.find_element(By.NAME, value="fName")
    fname.send_keys(first_name)

    lname = driver.find_element(By.NAME, value="lName")
    lname.send_keys(last_name)

    email = driver.find_element(By.NAME, value="email")
    email.send_keys(email_address)

    signup = driver.find_element(By.CSS_SELECTOR, value="button")
    signup.click()

if __name__ == "__main__":
    main()