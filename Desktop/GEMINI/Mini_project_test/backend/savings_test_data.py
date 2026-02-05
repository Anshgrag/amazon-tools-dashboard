"""
Smart Savings Test Data Generator for EcoTrack
Generates realistic data demonstrating cost savings from automation
"""

import requests
import random
import time
from datetime import datetime, timedelta

API_URL = "http://localhost:5000"
COST_PER_KWH = 0.12  # $0.12 per kWh

# Device configurations with waste patterns
DEVICES_CONFIG = {
    "TV": {
        "power_on": 120,           # watts
        "power_standby": 3,        # watts
        "voltage": 230,
        "waste_hours_per_day": 4,  # Hours left on when没人 watching
        "auto_saved_hours": 3,     # Hours automation saves
    },
    "Router": {
        "power_on": 15,            # watts (should be 24/7)
        "power_standby": 12,       # watts
        "voltage": 230,
        "waste_hours_per_day": 0,  # Router should always be on
        "auto_saved_hours": 0,     # No savings for router
    },
    "Charger": {
        "power_on": 25,            # watts (phone charging)
        "power_standby": 0.5,      # watts (left plugged in)
        "voltage": 230,
        "waste_hours_per_day": 8,  # Left plugged in unnecessarily
        "auto_saved_hours": 6,     # Automation unplug saves
    },
    "Refrigerator": {
        "power_on": 200,           # watts (compressor running)
        "power_standby": 50,       # watts (idle)
        "voltage": 230,
        "waste_hours_per_day": 2,  # Door left open, inefficient settings
        "auto_saved_hours": 1.5,   # Smart automation saves
    }
}

def calculate_cost(power_watts, hours):
    """Calculate cost for given power and duration"""
    power_kw = power_watts / 1000
    kwh = power_kw * hours
    return kwh * COST_PER_KWH

def generate_device_data(device_name, config, hours_ago=0):
    """Generate realistic device data for a specific time"""
    hour_of_day = (datetime.now().hour - hours_ago) % 24
    
    # Simulate different scenarios
    is_auto_controlled = random.random() < 0.3  # 30% chance automation was active
    is_manual_override = random.random() < 0.1  # 10% chance user overrode automation
    
    # Determine power state based on time and automation
    if device_name == "Router":
        # Router is always on
        power_watts = config["power_on"]
        mode = "ON"
    elif device_name == "Refrigerator":
        # Refrigerator cycles
        if random.random() < 0.7:  # 70% chance compressor is running
            power_watts = config["power_on"] if not is_auto_controlled else config["power_standby"]
            mode = "ON"
        else:
            power_watts = config["power_standby"]
            mode = "Standby"
    elif device_name == "TV":
        # TV usage patterns
        if 18 <= hour_of_day <= 23:  # Evening prime time
            if is_auto_controlled and random.random() < 0.4:  # 40% chance auto turned off
                power_watts = config["power_standby"]
                mode = "Standby"
                is_auto_controlled = True
            else:
                power_watts = config["power_on"]
                mode = "ON"
        else:  # Off hours
            idle_power = config.get("power_idle", 0.1)  # Default to very low power if not specified
            power_watts = config["power_standby"] if not is_auto_controlled else idle_power
            mode = "Standby"
    else:  # Charger
        # Charger patterns
        if 7 <= hour_of_day <= 9 or 19 <= hour_of_day <= 23:  # Charging times
            if is_auto_controlled and random.random() < 0.6:  # Smart charging
                power_watts = config["power_on"] if random.random() < 0.3 else config["power_standby"]
                mode = "ON" if power_watts > 5 else "Standby"
            else:
                power_watts = config["power_on"]
                mode = "ON"
        else:  # Should be off
            idle_power = config.get("power_idle", 0.1)  # Default to very low power if not specified
            power_watts = config["power_standby"] if not is_auto_controlled else idle_power
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

def add_device_events():
    """Add specific device waste/saved events"""
    print("📊 Adding device waste/saved events...")
    
    for device_name, config in DEVICES_CONFIG.items():
        # Calculate waste for the day
        waste_power = config["power_on"] - config["power_standby"]
        waste_hours = config["waste_hours_per_day"]
        saved_hours = config["auto_saved_hours"]
        
        if waste_hours > 0:
            # Add waste event (without automation)
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
                print(f"  ❌ {device_name}: ${result['cost_wasted']:.4f} wasted without automation")
        
        if saved_hours > 0:
            # Add saved event (with automation)
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
                print(f"  ✅ {device_name}: ${result['cost_wasted']:.4f} saved with automation")

def generate_historical_data(hours=24):
    """Generate historical data for the past N hours"""
    print(f"🔄 Generating {hours} hours of realistic device data...")
    
    for hours_ago in range(hours, 0, -1):
        for device_name, config in DEVICES_CONFIG.items():
            data = generate_device_data(device_name, config, hours_ago)
            
            response = requests.post(f"{API_URL}/api/electricity/add", json=data)
            if response.status_code == 201:
                power = data["power_watts"]
                auto = "🤖" if data["auto_controlled"] else "👤"
                mode = data["mode"]
                print(f"  {auto} {device_name} ({hours_ago}h ago): {power:.1f}W - {mode}")
            
            time.sleep(0.1)  # Small delay to avoid overwhelming the API

def show_savings_summary():
    """Display the savings summary"""
    print("\n📈 Fetching savings summary...")
    
    try:
        response = requests.get(f"{API_URL}/api/savings")
        if response.status_code == 200:
            data = response.json()
            if data["status"] == "success":
                savings = data["data"]
                print(f"\n💰 SMART SAVINGS SUMMARY:")
                print(f"  ❌ Wasted (Without Automation): ${savings['total_waste_cost']:.2f}")
                print(f"  ✅ Saved (With Automation): ${savings['total_saved_cost']:.2f}")
                print(f"  🎯 Net Savings: ${savings['net_savings']:.2f}")
                print(f"  ⚡ Cost per kWh: ${savings['cost_per_kwh']:.2f}")
                
                print(f"\n📱 DEVICE BREAKDOWN:")
                for device in savings["device_details"]:
                    net = device["saved_cost"] - device["waste_cost"]
                    icon = "✅" if net >= 0 else "❌"
                    print(f"  {icon} {device['device_name']}: {format(net, '+.2f')}")
    except Exception as e:
        print(f"❌ Error fetching savings: {e}")

def main():
    print("🚀 EcoTrack Smart Savings Test Data Generator")
    print("=" * 50)
    
    # First check if API is running
    try:
        response = requests.get(f"{API_URL}/")
        if response.status_code != 200:
            print("❌ API is not running. Please start the backend first.")
            return
    except:
        print("❌ Cannot connect to API. Please start the backend first.")
        return
    
    # Generate data
    generate_historical_data(24)
    add_device_events()
    
    # Show summary
    show_savings_summary()
    
    print(f"\n✅ Test data generation complete!")
    print(f"🌐 Open http://localhost:5000 to see your Smart Savings Monitor")

if __name__ == "__main__":
    main()