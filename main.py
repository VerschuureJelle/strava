# main.py

import strava_export
import energy_zones_config
import energy_burn
import os
from send_notification import send_strava_summary
import pandas as pd
from dotenv import load_dotenv

if __name__ == '__main__':
    load_dotenv()
    print("DEBUG: STRAVA_CLIENT_ID =", os.environ.get("STRAVA_CLIENT_ID"))
    print("🔄 Stap 1: Ophalen van nieuwe Strava-activiteiten...")
    strava_export.main()
    
    print("📊 Stap 2: Genereren of updaten van energieverbrandingsreferentie...")
    energy_zones_config  # Wordt alleen gebruikt om het CSV-bestand aan te maken indien nodig

    print("🔥 Stap 3: Berekening van macronutriëntenverbranding...")
    energy_burn  # Voert verrijking uit op activiteitenbestand
    print("✅ Alles afgerond via main.py")

# Laad laatste regel uit enriched bestand
df = pd.read_csv("strava_activities_enriched.csv")
last = df.sort_values("Date", ascending=False).iloc[0]

msg = (
    f"🏃‍♀️ Nieuwe {last['Type']} op {last['Date']}:\n"
    f"🔸 {round(last['Total Calories'])} kcal\n"
    f"🍞 KH: {round(last['Total Carbs (g)'])}g\n"
    f"🔥 Vet: {round(last['Total Fat (g)'])}g"
)
send_strava_summary(msg)