import requests
from datetime import datetime
import os

APP_ID = os.environ["NIX_APP_ID"]
API_KEY = os.environ["NIX_API_KEY"]

MY_WEIGHT_KG = 68
MY_HEIGHT_CM = 165.5
AGE = 21

MY_USERNAME = "shanelperera"
MY_PASSWORD = os.environ["SHEETY_WORKOUT_PASSWORD"]

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
sheet_endpoint = os.environ["SHEETY_WORKOUT_ENDPOINT"]

exercise_text = input("Tell me which exercises you did: ")

exercise_params = {
    "query": exercise_text,
    "weight_kg": MY_WEIGHT_KG,
    "height_cm": MY_HEIGHT_CM,
    "age": AGE
}

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY
}

response = requests.post(url=exercise_endpoint, json=exercise_params, headers=headers)
result = response.json()
print(result)

today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%H:%M:%S")

for exercise in result["exercises"]:
    sheet_inputs = {
        "workout" : {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

    sheet_response = requests.post(url=sheet_endpoint, json=sheet_inputs, auth=(MY_USERNAME, MY_PASSWORD))

    print(sheet_response.text)