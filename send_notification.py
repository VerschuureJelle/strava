# send_notification.py

import os
import pandas as pd
import requests
from dotenv import load_dotenv

# Specifiek pad naar jouw bestand
load_dotenv(dotenv_path="/Users/jelleverschuure/StravaEat/.env")

print("DEBUG: PUSHOVER_USER_KEY =", os.environ.get("PUSHOVER_USER_KEY"))
print("DEBUG: PUSHOVER_APP_TOKEN =", os.environ.get("PUSHOVER_APP_TOKEN"))

CSV_FILE = "strava_activities_enriched.csv"
NOTIFIED_FILE = "notified_ids.txt"

def load_notified_ids():
    if not os.path.exists(NOTIFIED_FILE):
        return set()
    with open(NOTIFIED_FILE, "r") as f:
        return set(line.strip() for line in f.readlines())

def save_notified_id(activity_id):
    with open(NOTIFIED_FILE, "a") as f:
        f.write(f"{activity_id}\n")

def get_activity_emoji(activity_type):
    emoji_map = {
        "Run": "🏃‍♂️",
        "Ride": "🚴‍♂️",
        "Swim": "🏊‍♂️",
    }
    return emoji_map.get(activity_type, "🏅")

def send_notification(activity):
    PUSHOVER_USER_KEY = os.environ.get("PUSHOVER_USER_KEY")
    PUSHOVER_APP_TOKEN = os.environ.get("PUSHOVER_APP_TOKEN")

    if not PUSHOVER_USER_KEY or not PUSHOVER_APP_TOKEN:
        raise RuntimeError("❌ Pushover keys ontbreken in de omgeving.")

    emoji = get_activity_emoji(activity['Type'])
    date_str = activity.get("FormattedDate") or pd.to_datetime(activity.get("Date")).strftime("%d-%m-%Y om %H:%M")
    afstand = activity.get("FormattedDistance", f"{activity['Distance (km)']:.1f} km")
    kcal = round(activity['Total Calories']) if pd.notna(activity['Total Calories']) else 'onbekend'
    vet = round(activity['Total Fat (g)']) if pd.notna(activity['Total Fat (g)']) else 'onbekend'
    kh = round(activity['Total Carbs (g)']) if pd.notna(activity['Total Carbs (g)']) else 'onbekend'

    title = f"{emoji} Nieuwe {activity['Type']} voltooid!"
    msg = (
        f"📅 Datum: {date_str}\n"
        f"📏 Afstand: {afstand}\n"
        f"🔥 Verbranding: {kcal} kcal\n"
        f"🍞 Koolhydraten: {kh}g\n"
        f"🥑 Vet: {vet}g"
    )

    response = requests.post("https://api.pushover.net/1/messages.json", data={
        "token": PUSHOVER_APP_TOKEN,
        "user": PUSHOVER_USER_KEY,
        "title": title,
        "message": msg,
        "priority": 0
    })
    if response.status_code == 200:
        print(f"✅ Melding verstuurd voor activiteit {activity['Activity ID']}")
    else:
        print(f"❌ Fout bij versturen: {response.text}")

def main():
    df = pd.read_csv(CSV_FILE)
    if 'Activity ID' not in df.columns:
        raise KeyError("Kolom 'Activity ID' ontbreekt in het CSV-bestand.")

    notified_ids = load_notified_ids()
    new_activities = df[~df['Activity ID'].astype(str).isin(notified_ids)]

    for _, activity in new_activities.iterrows():
        if pd.isna(activity["Total Calories"]):
            continue
        send_notification(activity)
        save_notified_id(str(activity["Activity ID"]))

if __name__ == "__main__":
    main()
