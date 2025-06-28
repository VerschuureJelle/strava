import requests
import pandas as pd
import os
from datetime import datetime

# === CONFIG ===
CLIENT_ID = os.environ["STRAVA_CLIENT_ID"]
CLIENT_SECRET = os.environ["STRAVA_CLIENT_SECRET"]
REFRESH_TOKEN = os.environ["STRAVA_REFRESH_TOKEN"]

CSV_FILE = 'strava_activities.csv'

# === CUSTOM HR ZONES PER SPORT ===
RUN_HR_ZONES = [0, 124, 135, 149, 161, 181, 200]    # Lopen
RIDE_HR_ZONES = [0, 102, 113, 131, 156, 169, 200]    # Fietsen

# === STEP 1: Get Access Token ===
def get_access_token():
    response = requests.post(
        'https://www.strava.com/oauth/token',
        data={
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'grant_type': 'refresh_token',
            'refresh_token': REFRESH_TOKEN
        }
    )
    if response.status_code != 200:
        print("❌ Access token ophalen mislukt:", response.text)
        return None
    return response.json().get('access_token')

# === STEP 2: Get Latest Activities ===
def get_latest_activities(token):
    url = 'https://www.strava.com/api/v3/athlete/activities'
    params = {'per_page': 10, 'page': 1}
    headers = {'Authorization': f'Bearer {token}'}

    res = requests.get(url, headers=headers, params=params)
    if res.status_code != 200:
        print("❌ Activiteiten ophalen mislukt:", res.text)
        return []
    return res.json()

# === STEP 3: Load existing CSV and get known IDs ===
def load_existing_ids():
    if os.path.exists(CSV_FILE):
        try:
            df = pd.read_csv(CSV_FILE)
            if 'Activity ID' in df.columns:
                return set(df['Activity ID'].astype(str))
        except pd.errors.EmptyDataError:
            print("📂 CSV-bestand is leeg — geen bekende activiteiten.")
    return set()

# === STEP 4: Get Full Activity Details ===
def get_activity_details(token, activity_id):
    url = f'https://www.strava.com/api/v3/activities/{activity_id}'
    headers = {'Authorization': f'Bearer {token}'}
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        print(f"❌ Fout bij ophalen details voor activiteit {activity_id}:", res.text)
        return {}
    return res.json()

# === STEP 5: Get Heart Rate Stream ===
def get_hr_stream(token, activity_id):
    url = f'https://www.strava.com/api/v3/activities/{activity_id}/streams'
    headers = {'Authorization': f'Bearer {token}'}
    params = {'keys': 'heartrate', 'key_by_type': 'true'}

    res = requests.get(url, headers=headers, params=params)
    if res.status_code != 200:
        print(f"⚠️ Geen hartslagdata voor activiteit {activity_id}:", res.text)
        return []
    return res.json().get('heartrate', {}).get('data', [])

# === STEP 6: Calculate Custom HR Zone Times (scaled to moving_time) ===
def calculate_hr_zone_times(hr_data, zone_bounds, moving_time):
    zone_counts = [0 for _ in range(len(zone_bounds) - 1)]
    for hr in hr_data:
        for i in range(len(zone_bounds) - 1):
            if zone_bounds[i] <= hr < zone_bounds[i + 1]:
                zone_counts[i] += 1
                break

    total_samples = sum(zone_counts)
    if total_samples == 0:
        return {f'Custom Zone {i+1} Time (sec)': 0 for i in range(len(zone_counts))}

    scale_factor = moving_time / total_samples
    scaled_zone_times = {f'Custom Zone {i+1} Time (sec)': round(zone_counts[i] * scale_factor) for i in range(len(zone_counts))}
    return scaled_zone_times

# === STEP 7: Extract and Save New Activities ===
def save_new_activities(new_activities):
    if not new_activities:
        print("✅ Geen nieuwe activiteiten om op te slaan.")
        return

    df = pd.DataFrame(new_activities)
    write_mode = 'a' if os.path.exists(CSV_FILE) else 'w'
    header = not os.path.exists(CSV_FILE)
    df.to_csv(CSV_FILE, mode=write_mode, header=header, index=False)
    print(f"✅ {len(df)} nieuwe activiteiten opgeslagen in {CSV_FILE}")

# === MAIN ===
def main():
    token = get_access_token()
    if not token:
        return

    activities = get_latest_activities(token)
    if not activities:
        return

    known_ids = load_existing_ids()
    new_data = []

    for act in activities:
        if str(act['id']) in known_ids:
            continue

        details = get_activity_details(token, act['id'])
        hr_stream = get_hr_stream(token, act['id'])

        activity_type = act.get('type')
        if activity_type == 'Run':
            zones = RUN_HR_ZONES
        elif activity_type == 'Ride':
            zones = RIDE_HR_ZONES
        else:
            zones = RUN_HR_ZONES  # default fallback

        moving_time = act.get('moving_time', 0)
        custom_zones = calculate_hr_zone_times(hr_stream, zones, moving_time)

        new_data.append({
            'Activity ID': act['id'],
            'Date': act.get('start_date_local'),
            'Name': act.get('name'),
            'Type': activity_type,
            'Distance (km)': act.get('distance', 0) / 1000,
            'Moving Time (min)': moving_time / 60,
            'Elapsed Time (min)': act.get('elapsed_time', 0) / 60,
            'Total Elevation Gain': act.get('total_elevation_gain', 0),
            'Avg HR': details.get('average_heartrate'),
            'Max HR': details.get('max_heartrate'),
            'Avg Power': details.get('average_watts'),
            'Max Power': details.get('max_watts'),
            **custom_zones
        })

    save_new_activities(new_data)

if __name__ == '__main__':
    main()
