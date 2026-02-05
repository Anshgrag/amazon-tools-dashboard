"""
Tuya IoT Platform Integration
Fetches real-time data from multiple Tuya smart plugs
"""

from tuya_connector import TuyaOpenAPI
import requests
import time
from datetime import datetime

# ==================== TUYA CREDENTIALS ====================
# Replace these with your actual Tuya IoT Platform credentials

ACCESS_ID = "your_access_id_here"          # From Tuya IoT Platform
ACCESS_KEY = "your_access_key_here"        # From Tuya IoT Platform
API_ENDPOINT = "https://openapi.tuyain.com"  # For India region
# Other regions:
# US: https://openapi.tuyaus.com
# EU: https://openapi.tuyaeu.com
# China: https://openapi.tuyacn.com

# Your device IDs (get from Tuya IoT Platform -> Devices tab)
DEVICE_IDS = [
    "device_id_1",  # TV Smart Plug
    "device_id_2",  # Router Smart Plug
    "device_id_3",  # Charger Smart Plug
    "device_id_4",  # Refrigerator Smart Plug
]

# Device name mapping
DEVICE_NAMES = {
    "device_id_1": "TV",
    "device_id_2": "Router",
    "device_id_3": "Charger",
    "device_id_4": "Refrigerator"
}

# Your Flask backend URL
BACKEND_URL = "http://localhost:5000"

# ==================== TUYA API CONNECTION ====================

def connect_to_tuya():
    """
    Connect to Tuya IoT Platform using your credentials
    """
    openapi = TuyaOpenAPI(API_ENDPOINT, ACCESS_ID, ACCESS_KEY)
    openapi.connect()
    print("✅ Connected to Tuya IoT Platform")
    return openapi

# ==================== FETCH DEVICE DATA ====================

def get_device_status(openapi, device_id):
    """
    Get current status and power consumption from a single device
    
    Returns data like:
    {
        "switch_1": True/False,
        "cur_power": 850,  # Current power in watts (multiply by 10)
        "cur_voltage": 2300,  # Voltage in 0.1V (230.0V)
        "cur_current": 400  # Current in mA (0.4A)
    }
    """
    try:
        response = openapi.get(f"/v1.0/devices/{device_id}/status")
        
        if response['success']:
            status_data = {}
            for item in response['result']:
                status_data[item['code']] = item['value']
            return status_data
        else:
            print(f"❌ Error fetching data for device {device_id}: {response}")
            return None
            
    except Exception as e:
        print(f"❌ Exception for device {device_id}: {e}")
        return None

def process_device_data(device_id, status_data):
    """
    Convert Tuya device data to EcoTrack format
    """
    device_name = DEVICE_NAMES.get(device_id, f"Device_{device_id[:8]}")
    
    # Extract power data (Tuya returns power in 0.1W, so divide by 10)
    cur_power = status_data.get('cur_power', 0) / 10  # Convert to watts
    cur_voltage = status_data.get('cur_voltage', 0) / 10  # Convert to volts
    switch_status = status_data.get('switch_1', False)
    
    # Determine mode
    if not switch_status:
        mode = "Idle"
    elif cur_power < 5:
        mode = "Standby"
    else:
        mode = "ON"
    
    return {
        "device_name": device_name,
        "mode": mode,
        "voltage": round(cur_voltage, 2),
        "power_watts": round(cur_power, 2),
        "timestamp": datetime.now().isoformat()
    }

def send_to_backend(data):
    """
    Send data to Flask backend API
    """
    try:
        response = requests.post(
            f"{BACKEND_URL}/api/electricity/add",
            json=data
        )
        if response.status_code == 201:
            print(f"✅ Sent data for {data['device_name']}: {data['power_watts']}W")
        else:
            print(f"❌ Failed to send data: {response.status_code}")
    except Exception as e:
        print(f"❌ Error sending data: {e}")

# ==================== MAIN LOOP ====================

def fetch_all_devices(openapi):
    """
    Fetch data from all registered Tuya devices
    """
    print(f"\n🔄 Fetching data from {len(DEVICE_IDS)} devices...")
    
    for device_id in DEVICE_IDS:
        status_data = get_device_status(openapi, device_id)
        
        if status_data:
            processed_data = process_device_data(device_id, status_data)
            send_to_backend(processed_data)
        
        time.sleep(0.5)  # Small delay between requests

def main():
    """
    Main function - continuously fetch data from Tuya devices
    """
    print("🚀 Starting Tuya IoT Integration...")
    print(f"📡 Backend URL: {BACKEND_URL}")
    print(f"🔌 Monitoring {len(DEVICE_IDS)} devices\n")
    
    # Connect to Tuya
    openapi = connect_to_tuya()
    
    # Continuous monitoring loop
    update_interval = 60  # Fetch data every 60 seconds
    
    try:
        while True:
            fetch_all_devices(openapi)
            print(f"⏳ Waiting {update_interval} seconds before next update...\n")
            time.sleep(update_interval)
    
    except KeyboardInterrupt:
        print("\n🛑 Stopping Tuya integration...")

if __name__ == "__main__":
    main()
