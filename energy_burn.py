# calculate_energy_burn.py

import pandas as pd
import os
from energy_zones_config import RUN_HR_ZONES, RIDE_HR_ZONES

ACTIVITY_FILE = 'strava_activities.csv'
RUN_REF_TABLE = 'hr_energy_reference_run.csv'
RIDE_REF_TABLE = 'hr_energy_reference_ride.csv'
OUT_FILE = 'strava_activities_enriched.csv'

# Stap 1: Laad bestaande gegevens
activities = pd.read_csv(ACTIVITY_FILE)
run_ref = pd.read_csv(RUN_REF_TABLE).sort_values(by='Heart Rate').reset_index(drop=True)
ride_ref = pd.read_csv(RIDE_REF_TABLE).sort_values(by='Heart Rate').reset_index(drop=True)

# Voeg kolommen toe als ze nog niet bestaan
for col in ['Total Carbs (g)', 'Total Fat (g)', 'Total Calories']:
    if col not in activities.columns:
        activities[col] = None

# Herbereken alleen voor nieuwe activiteiten
new_rows = activities[activities['Total Carbs (g)'].isna()]

print(f"🔍 Activiteiten zonder verbranding: {len(new_rows)}")

for idx, row in new_rows.iterrows():
    sport = row['Type']
    total_carbs = 0
    total_fat = 0
    total_calories = 0

    if sport == 'Ride':
        zones = RIDE_HR_ZONES
        ref = ride_ref
    elif sport == 'Run':
        zones = RUN_HR_ZONES
        ref = run_ref
    else:
        print(f"⚠️ Onbekend activiteitstype: {sport} — overslaan")
        continue

    for zone_num in range(1, len(zones)):
        zone_col = f'Custom Zone {zone_num} Time (sec)'
        if zone_col not in row or pd.isna(row[zone_col]):
            continue

        hr_avg = (zones[zone_num - 1] + zones[zone_num]) / 2

        # Zoek dichtstbijzijnde HR in referentie
        closest_idx = (ref['Heart Rate'] - hr_avg).abs().idxmin()
        ref_row = ref.loc[closest_idx]

        # Tijd in uren
        hours = row[zone_col] / 3600

        total_carbs += ref_row['Carbs per hour'] * hours
        total_fat += ref_row['Fat per hour'] * hours
        total_calories += ref_row['Calories per hour'] * hours

    # Waarden bijwerken
    activities.at[idx, 'Total Carbs (g)'] = round(total_carbs, 2)
    activities.at[idx, 'Total Fat (g)'] = round(total_fat, 2)
    activities.at[idx, 'Total Calories'] = round(total_calories, 2)

# Opslaan
activities.to_csv(OUT_FILE, index=False)
print(f"✅ Uitgebreide activiteiten opgeslagen in {OUT_FILE}")
