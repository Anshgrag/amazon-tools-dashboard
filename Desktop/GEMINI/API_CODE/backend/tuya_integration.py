"""
Tuya IoT Platform Integration
Fetches real-time data from Tuya smart switches using tinytuya
"""

import tinytuya
import requests
import time
from datetime import datetime
import json

# ==================== TUYA CREDENTIALS ====================
# Load credentials from tinytuya.json
try:
    with open('../tinytuya.json', 'r') as f:
        config = json.load(f)
    ACCESS_ID = config['apiKey']
    ACCESS_SECRET = config['apiSecret']
    API_REGION = config['apiRegion']
    DEVICE_ID = config['apiDeviceID']
except FileNotFoundError:
    print("❌ tinytuya.json not found. Please ensure it's in the project root.")
    exit(1)

# Device configuration
DEVICE_IDS = [DEVICE_ID]
DEVICE_NAMES = {
    DEVICE_ID: "Smart Switch"
}

# Your Flask backend URL
BACKEND_URL = "http://localhost:5000"

# ==================== TUYA API CONNECTION ====================

def connect_to_tuya():
    """
    Connect to Tuya IoT Platform using tinytuya
    """
    try:
        cloud = tinytuya.Cloud(apiRegion=API_REGION, apiKey=ACCESS_ID, apiSecret=ACCESS_SECRET)
        print("✅ Connected to Tuya Cloud")
        return cloud
    except Exception as e:
        print(f"❌ Failed to connect to Tuya Cloud: {e}")
        return None

# ==================== FETCH DEVICE DATA ====================

def get_device_status(cloud, device_id):
    """
    Get current status and power consumption from a single device using tinytuya

    Returns data like:
    {
        "switch_1": True/False,
        "cur_power": 850,  # Current power in 0.1W
        "cur_voltage": 2300,  # Voltage in 0.1V
        "cur_current": 400  # Current in mA
    }
    """
    try:
        # Get device status from cloud
        devices = cloud.getdevices()
        device = next((d for d in devices if d['id'] == device_id), None)

        if not device:
            print(f"❌ Device {device_id} not found in cloud")
            return None

        # Get detailed status
        response = cloud.getstatus(device_id)
        if response and response.get('success'):
            status_list = response.get('result', [])
            status_data = {}
            for item in status_list:
                if isinstance(item, dict):
                    status_data[item.get('code', '')] = item.get('value', '')
            print(f"Status data: {status_data}")  # Debug
            return status_data
        else:
            print(f"❌ Failed to get status for device {device_id}: {response}")
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

def fetch_all_devices(cloud):
    """
    Fetch data from all registered Tuya devices
    """
    print(f"\n🔄 Fetching data from {len(DEVICE_IDS)} devices...")

    for device_id in DEVICE_IDS:
        status_data = get_device_status(cloud, device_id)

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
    cloud = connect_to_tuya()
    if not cloud:
        print("❌ Cannot proceed without Tuya connection")
        return

    # Continuous monitoring loop
    update_interval = 60  # Fetch data every 60 seconds

    try:
        while True:
            fetch_all_devices(cloud)
            print(f"⏳ Waiting {update_interval} seconds before next update...\n")
            time.sleep(update_interval)

    except KeyboardInterrupt:
        print("\n🛑 Stopping Tuya integration...")

if __name__ == "__main__":
    main()
