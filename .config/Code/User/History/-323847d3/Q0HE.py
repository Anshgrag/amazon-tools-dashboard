import requests
import random
from datetime import datetime

API_URL = "http://localhost:5000"

# Add sample AQI data
for i in range(10):
    requests.post(f"{API_URL}/api/aqi/add", json={
        "location_type": "indoor",
        "aqi_value": random.randint(30, 80),
        "timestamp": datetime.now().isoformat()
    })

# Add sample electricity data
devices = ["TV", "Router", "Charger", "Refrigerator"]
modes = ["ON", "Standby", "Idle"]

for device in devices:
    requests.post(f"{API_URL}/api/electricity/add", json={
        "device_name": device,
        "mode": random.choice(modes),
        "voltage": round(random.uniform(220, 240), 2),
        "power_watts": round(random.uniform(10, 150), 2),
        "timestamp": datetime.now().isoformat()
    })

print("✅ Sample data added successfully!")
