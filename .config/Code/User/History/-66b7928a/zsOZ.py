"""
Real-time Regional AQI Integration
Fetches live AQI data from WAQI (World Air Quality Index)
Works for ANY city in India without physical sensors!
"""

import requests
import time
from datetime import datetime

# ==================== CONFIGURATION ====================

# Your WAQI API Token (get from: https://aqicn.org/data-platform/token/)
WAQI_API_TOKEN = "465b3b09f08acc38dbe25719ea686a48d950c735"  # Replace with your actual token

# Your city name
CITY = "hosur"  # Can be: hosur, bangalore, delhi, mumbai, etc.

# Backend URL
BACKEND_URL = "http://localhost:5000"

# Update interval (seconds)
UPDATE_INTERVAL = 300  # 5 minutes (to stay within free tier limits)

# ==================== WAQI API FUNCTIONS ====================

def get_city_aqi(city_name):
    """
    Fetch real-time AQI data for a specific city
    API Documentation: https://aqicn.org/json-api/doc/
    
    Returns:
    {
        "aqi": 85,
        "dominant_pollutant": "pm25",
        "timestamp": "2026-01-08T13:00:00",
        "city": "Hosur, India",
        "pollutants": {...}
    }
    """
    url = f"http://api.waqi.info/feed/{city_name}/?token={WAQI_API_TOKEN}"
    
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if data['status'] == 'ok':
            aqi_data = data['data']
            
            return {
                "aqi": aqi_data.get('aqi', 0),
                "dominant_pollutant": aqi_data.get('dominentpol', 'unknown'),
                "timestamp": aqi_data['time']['iso'],
                "city": aqi_data['city']['name'],
                "pollutants": {
                    "pm25": aqi_data.get('iaqi', {}).get('pm25', {}).get('v', None),
                    "pm10": aqi_data.get('iaqi', {}).get('pm10', {}).get('v', None),
                    "o3": aqi_data.get('iaqi', {}).get('o3', {}).get('v', None),
                    "no2": aqi_data.get('iaqi', {}).get('no2', {}).get('v', None),
                    "co": aqi_data.get('iaqi', {}).get('co', {}).get('v', None)
                }
            }
        else:
            print(f"❌ API Error: {data.get('data', 'Unknown error')}")
            return None
            
    except Exception as e:
        print(f"❌ Error fetching AQI: {e}")
        return None

def get_nearby_aqi():
    """
    Get AQI based on your IP location (automatic)
    Useful if city name doesn't work
    """
    url = f"http://api.waqi.info/feed/here/?token={WAQI_API_TOKEN}"
    
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if data['status'] == 'ok':
            return data['data']
        else:
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def get_coordinates_aqi(lat, lon):
    """
    Get AQI for specific GPS coordinates
    Example: get_coordinates_aqi(12.7342, 77.8294)  # Hosur coordinates
    """
    url = f"http://api.waqi.info/feed/geo:{lat};{lon}/?token={WAQI_API_TOKEN}"
    
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if data['status'] == 'ok':
            return data['data']
        else:
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

# ==================== SEND TO BACKEND ====================

def send_outdoor_aqi(aqi_value):
    """
    Send outdoor AQI data to Flask backend
    """
    data = {
        "location_type": "outdoor",
        "aqi_value": aqi_value,
        "timestamp": datetime.now().isoformat()
    }
    
    try:
        response = requests.post(f"{BACKEND_URL}/api/aqi/add", json=data)
        if response.status_code == 201:
            print(f"✅ Outdoor AQI sent: {aqi_value}")
            return True
        else:
            print(f"❌ Failed to send outdoor AQI: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error sending data: {e}")
        return False

def send_indoor_aqi(outdoor_aqi):
    """
    Estimate indoor AQI (typically 30-50% better than outdoor)
    """
    # Indoor AQI is usually better due to filtration
    indoor_aqi = int(outdoor_aqi * 0.6)  # 40% reduction from outdoor
    
    data = {
        "location_type": "indoor",
        "aqi_value": indoor_aqi,
        "timestamp": datetime.now().isoformat()
    }
    
    try:
        response = requests.post(f"{BACKEND_URL}/api/aqi/add", json=data)
        if response.status_code == 201:
            print(f"✅ Indoor AQI sent: {indoor_aqi}")
            return True
        else:
            print(f"❌ Failed to send indoor AQI: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error sending data: {e}")
        return False

# ==================== MAIN LOOP ====================

def main():
    """
    Continuously fetch real-time AQI data and send to backend
    """
    print("\n" + "=" * 60)
    print("  🌍 LIVE REGIONAL AQI INTEGRATION")
    print("=" * 60)
    print(f"  City: {CITY.upper()}")
    print(f"  Update Interval: {UPDATE_INTERVAL} seconds")
    print(f"  Backend: {BACKEND_URL}")
    print("=" * 60 + "\n")
    
    # Test API connection
    print("🔍 Testing API connection...")
    test_data = get_city_aqi(CITY)
    
    if test_data:
        print(f"✅ API Connected! Current AQI: {test_data['aqi']}")
        print(f"   City: {test_data['city']}")
        print(f"   Dominant Pollutant: {test_data['dominant_pollutant']}")
    else:
        print("❌ Failed to connect to API. Check your token and city name.")
        print("\nTrying auto-location based on IP...")
        test_data = get_nearby_aqi()
        if test_data:
            print(f"✅ Auto-location worked! AQI: {test_data.get('aqi')}")
            print(f"   Location: {test_data['city']['name']}")
        else:
            print("❌ Auto-location also failed. Please check your API token.")
            return
    
    print("\n🔄 Starting continuous monitoring...\n")
    
    iteration = 0
    
    try:
        while True:
            iteration += 1
            print(f"\n⏱️  Update #{iteration} - {datetime.now().strftime('%I:%M:%S %p')}")
            print("-" * 60)
            
            # Fetch real-time AQI
            aqi_data = get_city_aqi(CITY)
            
            if aqi_data:
                outdoor_aqi = aqi_data['aqi']
                
                print(f"🌍 {aqi_data['city']}")
                print(f"   Outdoor AQI: {outdoor_aqi}")
                print(f"   Dominant Pollutant: {aqi_data['dominant_pollutant'].upper()}")
                
                # Show pollutant breakdown
                if aqi_data['pollutants']['pm25']:
                    print(f"   PM2.5: {aqi_data['pollutants']['pm25']}")
                if aqi_data['pollutants']['pm10']:
                    print(f"   PM10: {aqi_data['pollutants']['pm10']}")
                
                # Send to backend
                send_outdoor_aqi(outdoor_aqi)
                send_indoor_aqi(outdoor_aqi)
                
            else:
                print("⚠️  Failed to fetch AQI data this cycle")
            
            print(f"\n⏳ Next update in {UPDATE_INTERVAL} seconds...")
            print("-" * 60)
            time.sleep(UPDATE_INTERVAL)
            
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping AQI monitoring...")
        print("Goodbye! 👋\n")

if __name__ == "__main__":
    main()
