import pandas as pd
import os
import requests

CSV_FILE = "strava_activities_enriched.csv"
NOTIFIED_FILE = "notified_ids.txt"

PUSHOVER_USER_KEY = os.environ["PUSHOVER_USER_KEY"]
PUSHOVER_APP_TOKEN = os.environ["PUSHOVER_API_TOKEN"]

def load_notified_ids():
    if not os.path.exists(NOTIFIED_FILE):
        return set()
    with open(NOTIFIED_FILE, "r") as f:
        return set(line.strip() for line in f.readlines())

def save_notified_id(activity_id):
    with open(NOTIFIED_FILE, "a") as f:
        f.write(f"{activity_id}\n")

def send_notification(activity):
    title = f"🏃‍♂️ Nieuwe {activity['Type']}: {int(activity['Total Calories'])} kcal"
    msg = (
        f"Afstand: {activity['Distance (km)']} km\n"
        f"Vet: {round(activity['Total Fat (g)'])}g\n"
        f"Koolhydraten: {round(activity['Total Carbs (g)'])}g"
    )
    response = requests.post("https://api.pushover.net/1/messages.json", data={
        "token": PUSHOVER_APP_TOKEN,
        "user": PUSHOVER_USER_KEY,
        "title": title,
        "message": msg,
        "priority": 0
    })
    if response.status_code == 200:
        print(f"✅ Melding verstuurd voor activiteit {activity['ID']}")
    else:
        print(f"❌ Fout bij versturen: {response.text}")

def main():
    df = pd.read_csv(CSV_FILE)
    notified_ids = load_notified_ids()

    new_activities = df[~df['ID'].astype(str).isin(notified_ids)]

    for _, activity in new_activities.iterrows():
        if pd.isna(activity["Total Calories"]):
            continue
        send_notification(activity)
        save_notified_id(str(activity["ID"]))

if __name__ == "__main__":
    main()
