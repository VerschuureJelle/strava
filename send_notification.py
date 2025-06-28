# send_notification.py
import requests

PUSHOVER_USER_KEY = 'u38au9fvkphz3mkb1x9hrithpmb49s'
PUSHOVER_API_TOKEN = 'a2t3d626y7xb3c182ksepbpykys3ct'

def send_strava_summary(message: str):
    response = requests.post(
        "https://api.pushover.net/1/messages.json",
        data={
            "token": PUSHOVER_API_TOKEN,
            "user": PUSHOVER_USER_KEY,
            "message": message
        }
    )
    if response.status_code == 200:
        print("✅ Notificatie verzonden.")
    else:
        print(f"❌ Fout bij verzenden notificatie: {response.text}")
