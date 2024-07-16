import requests
from datetime import datetime
import os

ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/exercise"
sheety_endpoint = os.environ["sheety_endpoint"]

exercise_text = input("Which exercise did you do?")
GENDER = "male"
AGE = 18
HEIGHT_CM = 180
WEIGHT_KG = 60

APP_ID = os.environ["NT_APP_ID"]
APP_KEY = os.environ["NI_APP_KEY"]

headers = {
    "x-app-id": APP_ID,
    "x-app-key": APP_KEY,
}
nutrition_params = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE,
}
response = requests.post(url=ENDPOINT, json=nutrition_params, headers=headers)
response.raise_for_status()
result = response.json()

today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

bearer_headers = {
    "Authorization": "Bearer 6688diggy"
}

for exercise in result["exercises"]:
    sheet_inputs = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

    sheet_response = requests.post(sheety_endpoint, json=sheet_inputs, headers=bearer_headers )

    print(sheet_response.text)
