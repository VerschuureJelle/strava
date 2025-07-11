# main.py
from dotenv import load_dotenv  
import os
import strava_export
import energy_zones_config
import energy_burn
import send_notification

load_dotenv()
if __name__ == '__main__':
    print("🔄 Stap 1: Ophalen van nieuwe Strava-activiteiten...")
    strava_export.main()
    
    print("📊 Stap 2: Genereren of updaten van energieverbrandingsreferentie...")
    energy_zones_config  # Wordt alleen gebruikt om het CSV-bestand aan te maken indien nodig

    print("🔥 Stap 3: Berekening van macronutriëntenverbranding...")
    energy_burn  # Voert verrijking uit op activiteitenbestand

    print("📲 Stap 4: Verstuur pushnotificaties voor nieuwe activiteiten...")
    send_notification.main()

    print("✅ Alle stappen voltooid!")