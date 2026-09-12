import requests
from datetime import datetime
import smtplib
import time

MY_LAT = 7.082892 # Your latitude
MY_LONG = 79.868396 # Your longitude

MY_EMAIL = "gtest4py@gmail.com"
MY_PASSWORD = "wwhq svkw vjac qpgq"

def main():
    time.sleep(60)
    while True:
        if is_iss_overhead() and is_night():
            send_email()

def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    #Your position is within +5 or -5 degrees of the ISS position.
    if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LONG - 5 <= iss_longitude <= MY_LONG + 5:
        return True

def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour

    if time_now >= sunset or time_now <= sunrise:
        return True

def send_email():
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL, to_addrs="shanelradperera@gmail.com", msg="Subject:Look Up👆\n\nThe ISS is above you in the sky.")

# BONUS: run the code every 60 seconds.

if __name__ == "__main__":
    main()


