import requests
import random
import time
from datetime import datetime, timedelta

API_URL = "http://localhost:5000"

def add_sample_data():
    print("🔄 Adding sample data to EcoTrack...")
    
    # Add AQI data (indoor and outdoor) for last 24 hours
    print("\n📊 Adding AQI data...")
    for i in range(20):
        # Indoor AQI
        indoor_response = requests.post(f"{API_URL}/api/aqi/add", json={
            "location_type": "indoor",
            "aqi_value": random.randint(30, 90),
            "timestamp": (datetime.now() - timedelta(hours=i)).isoformat()
        })
        print(f"  ✓ Indoor AQI {i+1}: {indoor_response.status_code}")
        
        # Outdoor AQI
        outdoor_response = requests.post(f"{API_URL}/api/aqi/add", json={
            "location_type": "outdoor",
            "aqi_value": random.randint(50, 150),
            "timestamp": (datetime.now() - timedelta(hours=i)).isoformat()
        })
        print(f"  ✓ Outdoor AQI {i+1}: {outdoor_response.status_code}")
        
        time.sleep(0.1)  # Small delay to avoid overwhelming the server
    
    # Add electricity data for different devices
    print("\n⚡ Adding electricity data...")
    devices = [
        {"name": "TV", "power_range": (80, 150), "voltage": 230},
        {"name": "Router", "power_range": (10, 20), "voltage": 230},
        {"name": "Charger", "power_range": (5, 15), "voltage": 230},
        {"name": "Refrigerator", "power_range": (100, 200), "voltage": 230}
    ]
    
    modes = ["ON", "Standby", "Idle"]
    
    for device in devices:
        for i in range(15):
            mode = random.choice(modes)
            power = random.uniform(*device["power_range"])
            
            # Reduce power for Standby and Idle modes
            if mode == "Standby":
                power = power * 0.3
            elif mode == "Idle":
                power = power * 0.1
            
            response = requests.post(f"{API_URL}/api/electricity/add", json={
                "device_name": device["name"],
                "mode": mode,
                "voltage": round(random.uniform(device["voltage"] - 10, device["voltage"] + 10), 2),
                "power_watts": round(power, 2),
                "timestamp": (datetime.now() - timedelta(hours=i)).isoformat()
            })
            print(f"  ✓ {device['name']} reading {i+1}: {response.status_code}")
            
            time.sleep(0.1)
    
    print("\n✅ Sample data added successfully!")
    print("🌐 Open http://localhost:8000 to view the dashboard")

if __name__ == "__main__":
    try:
        # Check if backend is running
        response = requests.get(f"{API_URL}/")
        if response.status_code == 200:
            add_sample_data()
        else:
            print("❌ Backend is not responding correctly")
    except requests.exceptions.ConnectionError:
        print("❌ Error: Backend server is not running!")
        print("Please start the backend first using: python app.py")
