# energy_zones_config.py

import pandas as pd

heart_rates_run = [0,107,122,126,127,132,134,136,140,142,143,146,147,151,153,154,157,160,161,163,165,167,168,171,173,174,178,181]
heart_rates_ride = [0, 92, 95, 104, 106, 112, 118, 122, 126, 132, 138, 142, 148, 153, 158, 163, 168, 185]
# === Handmatige invoer: hardlopen ===
run_data = pd.DataFrame({
    'Heart Rate': heart_rates_run,
    'Carbs per hour': [0, 61, 95, 115, 126,133,128, 139, 167, 165, 158, 173, 166, 188, 204, 194, 209, 218, 206, 231, 244, 243, 244, 253, 248, 251, 264, 270],
    'Fat per hour': [0, 13, 26, 19, 16, 16, 18, 17, 9, 9, 15, 11, 16, 8, 3, 10, 5, 4, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'Calories per hour': [0, 412, 698, 716, 740, 765, 769, 805, 839, 867, 893, 917, 932, 957, 975, 1001, 1025, 1003, 1041, 1100, 1091, 1100, 1143, 1118, 1135, 1192, 1221, 1250]
})

# === Handmatige invoer: fietsen ===
ride_data = pd.DataFrame({
    'Heart Rate': heart_rates_ride,
    'Carbs per hour': [0, 25, 75, 87, 96, 104, 128, 134, 139, 172, 184, 209, 226, 231, 249, 257, 268, 272],
    'Fat per hour': [0, 23, 8, 12, 8, 12, 8, 8, 9, 3, 2, 0, 0, 0, 0, 0, 0, 0],
    'Calories per hour': [0, 347, 425, 510, 512, 590, 664, 685, 725, 812, 849, 942, 1010, 1043, 1127, 1162, 1200, 1229]
})

# === Validatie ===
assert run_data.shape[1] == 4 and ride_data.shape[1] == 4, "❌ Zorg dat elke sport exact 4 kolommen heeft"

run_data.to_csv("hr_energy_reference_run.csv", index=False)
ride_data.to_csv("hr_energy_reference_ride.csv", index=False)

# Zones voor later hergebruik (bijv. berekening in energy_burn)
RUN_HR_ZONES = [0, 124, 135, 149, 161, 181, 200]
RIDE_HR_ZONES = [0, 102, 113, 131, 156, 169, 200]

print("✅ Referentiebestanden succesvol aangemaakt.")
