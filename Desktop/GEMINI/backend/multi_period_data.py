"""
Multi-Period Smart Savings Test Data Generator
Generates data for different time periods to test filtering
"""

import requests
import random
import time
from datetime import datetime, timedelta

API_URL = "http://localhost:5000"
COST_PER_KWH = 0.12

# Device configurations
DEVICES_CONFIG = {
    "TV": {"power_on": 120, "power_standby": 3, "voltage": 230},
    "Router": {"power_on": 15, "power_standby": 12, "voltage": 230},
    "Charger": {"power_on": 25, "power_standby": 0.5, "voltage": 230},
    "Refrigerator": {"power_on": 200, "power_standby": 50, "voltage": 230}
}

def generate_device_data(device_name, config, hours_ago=0, period='month'):
    """Generate device data for specific time period"""
    hour_of_day = (datetime.now().hour - hours_ago) % 24
    
    # Determine if data should be included based on period
    days_ago = hours_ago // 24
    
    if period == 'today' and days_ago >= 1:
        return None
    elif period == 'month' and days_ago >= 30:
        return None
    elif period == 'year' and days_ago >= 365:
        return None
    
    # Simulate different scenarios
    is_auto_controlled = random.random() < 0.3
    is_manual_override = random.random() < 0.1
    
    # Determine power state based on time and automation
    if device_name == "Router":
        power_watts = config["power_on"]
        mode = "ON"
    elif device_name == "Refrigerator":
        if random.random() < 0.7:
            power_watts = config["power_on"] if not is_auto_controlled else config["power_standby"]
            mode = "ON"
        else:
            power_watts = config["power_standby"]
            mode = "Standby"
    elif device_name == "TV":
        if 18 <= hour_of_day <= 23 and days_ago == 0:  # Evening today
            if is_auto_controlled and random.random() < 0.4:
                power_watts = config["power_standby"]
                mode = "Standby"
                is_auto_controlled = True
            else:
                power_watts = config["power_on"]
                mode = "ON"
        else:
            power_watts = config["power_standby"]
            mode = "Standby"
    else:  # Charger
        if 7 <= hour_of_day <= 9 or 19 <= hour_of_day <= 23:  # Charging times
            if is_auto_controlled and random.random() < 0.6:
                power_watts = config["power_standby"]
                mode = "Standby"
                is_auto_controlled = True
            else:
                power_watts = config["power_on"]
                mode = "ON"
        else:
            power_watts = config["power_standby"]
            mode = "Standby"
    
    return {
        "device_name": device_name,
        "mode": mode,
        "voltage": config["voltage"] + random.uniform(-5, 5),
        "power_watts": power_watts + random.uniform(-2, 2),
        "timestamp": (datetime.now() - timedelta(hours=hours_ago)).isoformat(),
        "auto_controlled": is_auto_controlled,
        "manual_override": is_manual_override
    }

def generate_period_data(period, hours_to_generate):
    """Generate data for specific period"""
    print(f"🔄 Generating {hours_to_generate} hours of data for {period.upper()}...")
    
    for hours_ago in range(hours_to_generate, 0, -1):
        for device_name, config in DEVICES_CONFIG.items():
            data = generate_device_data(device_name, config, hours_ago, period)
            
            if data:  # Only add if data should be included for this period
                response = requests.post(f"{API_URL}/api/electricity/add", json=data)
                if response.status_code == 201:
                    auto = "🤖" if data["auto_controlled"] else "👤"
                    mode = data["mode"]
                    power = data["power_watts"]
                    print(f"  {auto} {device_name} ({hours_ago}h ago): {power:.1f}W - {mode}")
                else:
                    print(f"  ❌ Failed to add data for {device_name}")
        
        time.sleep(0.05)  # Small delay to avoid overwhelming API
    
    print(f"✅ {period.upper()} data generation complete!")

def add_device_events(period):
    """Add device events for specific period"""
    print(f"📊 Adding {period} device events...")
    
    for device_name, config in DEVICES_CONFIG.items():
        waste_power = config["power_on"] - config["power_standby"]
        
        # Adjust waste/saved hours based on period
        if period == 'today':
            waste_hours = random.uniform(2, 4)
            saved_hours = random.uniform(1, 2)
        elif period == 'month':
            waste_hours = random.uniform(60, 120)
            saved_hours = random.uniform(30, 60)
        elif period == 'year':
            waste_hours = random.uniform(730, 1460)
            saved_hours = random.uniform(365, 730)
        else:
            waste_hours = 60
            saved_hours = 30
        
        # Add waste event
        waste_event = {
            "device_name": device_name,
            "event_type": "waste",
            "power_watts": waste_power,
            "duration_minutes": int(waste_hours * 60),
            "auto_saved": False,
            "timestamp": (datetime.now() - timedelta(hours=12)).isoformat()
        }
        
        response = requests.post(f"{API_URL}/api/device-event", json=waste_event)
        if response.status_code == 201:
            result = response.json()
            print(f"  ❌ {device_name}: ${result['cost_wasted']:.4f} wasted")
        
        # Add saved event (if significant)
        if saved_hours > 1:
            saved_event = {
                "device_name": device_name,
                "event_type": "saved",
                "power_watts": waste_power,
                "duration_minutes": int(saved_hours * 60),
                "auto_saved": True,
                "timestamp": (datetime.now() - timedelta(hours=6)).isoformat()
            }
            
            response = requests.post(f"{API_URL}/api/device-event", json=saved_event)
            if response.status_code == 201:
                result = response.json()
                print(f"  ✅ {device_name}: ${result['cost_wasted']:.4f} saved")

def test_period_filtering():
    """Test that period filtering works correctly"""
    print("\n🔍 Testing Period Filtering...")
    
    periods = ['today', 'month', 'year']
    for period in periods:
        try:
            response = requests.get(f"{API_URL}/api/savings?period={period}")
            if response.status_code == 200:
                result = response.json()
                if result["status"] == "success":
                    data = result["data"]
                    print(f"  ✅ {period.upper()}: Waste=${data['total_waste_cost']:.2f}, Saved=${data['total_saved_cost']:.2f}")
                else:
                    print(f"  ❌ {period.upper()}: API error")
            else:
                print(f"  ❌ {period.upper()}: HTTP {response.status_code}")
        except Exception as e:
            print(f"  ❌ {period.upper()}: {e}")

def main():
    print("🚀 Multi-Period Smart Savings Test Data Generator")
    print("=" * 60)
    
    # Check if API is running
    try:
        response = requests.get(f"{API_URL}/")
        if response.status_code != 200:
            print("❌ API is not running. Please start the backend first.")
            return
    except:
        print("❌ Cannot connect to API. Please start the backend first.")
        return
    
    # Generate data for all periods
    periods_to_generate = {
        'today': 24,
        'month': 24 * 7,  # 1 week of data
        'year': 24 * 2     # 2 days of data
    }
    
    for period, hours in periods_to_generate.items():
        generate_period_data(period, hours)
        add_device_events(period)
        print()
    
    # Test filtering
    test_period_filtering()
    
    print(f"\n✅ Multi-period data generation complete!")
    print(f"🌐 Open http://localhost:8000 to test the time filter tabs")
    print(f"\n📊 Available periods:")
    for period in ['today', 'month', 'year']:
        print(f"  - {period.upper()}: http://localhost:5000/api/savings?period={period}")

if __name__ == "__main__":
    main()