"""
Advanced Test Data Generator for EcoTrack
Generates realistic electricity and AQI data based on:
- Real household power consumption patterns
- Daily usage cycles (morning, afternoon, evening, night)
- Indian AQI pollution levels
- Device-specific behavior patterns

Data Sources:
- US EIA Average Household Consumption Data
- Indian AQI Real-time Pollution Levels
- Appliance Power Consumption Standards
"""

import requests
import random
import time
from datetime import datetime, timedelta
import math

API_URL = "http://localhost:5000"

# ==================== REALISTIC DEVICE CONFIGURATIONS ====================

# Based on US Energy Information Administration data
DEVICES_CONFIG = {
    "TV": {
        "power_on": (85, 150),          # 40-55 inch LED TV (watts)
        "power_standby": (2, 5),        # Standby consumption
        "power_idle": (0.5, 1),         # Off but plugged in
        "voltage": (220, 240),          # Voltage range in India
        "typical_hours": {
            "morning": 0.3,   # 30% chance ON in morning
            "afternoon": 0.2, # 20% chance ON in afternoon
            "evening": 0.9,   # 90% chance ON in evening
            "night": 0.1      # 10% chance ON at night
        },
        "color": "#ff6b9d"
    },
    "Refrigerator": {
        "power_on": (150, 250),         # Running (compressor active)
        "power_standby": (40, 60),      # Idle (compressor off)
        "power_idle": (40, 60),         # Always on minimum
        "voltage": (220, 240),
        "typical_hours": {
            "morning": 0.8,   # 80% running (door opened frequently)
            "afternoon": 0.6, # 60% running
            "evening": 0.7,   # 70% running (dinner prep)
            "night": 0.4      # 40% running (low activity)
        },
        "color": "#ffd166"
    },
    "Router": {
        "power_on": (8, 15),            # WiFi router active
        "power_standby": (8, 15),       # Always on (no standby)
        "power_idle": (8, 15),          # No idle state
        "voltage": (220, 240),
        "typical_hours": {
            "morning": 1.0,   # Always ON
            "afternoon": 1.0,
            "evening": 1.0,
            "night": 1.0
        },
        "color": "#c77dff"
    },
    "Charger": {
        "power_on": (10, 25),           # Phone/laptop charging
        "power_standby": (0.5, 2),      # Plugged in, not charging
        "power_idle": (0.2, 0.5),       # Energy vampire
        "voltage": (220, 240),
        "typical_hours": {
            "morning": 0.5,   # 50% charging in morning
            "afternoon": 0.2, # 20% charging
            "evening": 0.6,   # 60% charging
            "night": 0.8      # 80% charging overnight
        },
        "color": "#4ecdc4"
    },
    "Washing Machine": {
        "power_on": (400, 800),         # Washing/spinning
        "power_standby": (2, 5),        # Display panel only
        "power_idle": (0.5, 1),         # Off
        "voltage": (220, 240),
        "typical_hours": {
            "morning": 0.4,   # 40% used in morning
            "afternoon": 0.1, # 10% used
            "evening": 0.05,  # 5% used
            "night": 0.0      # Never at night
        },
        "color": "#06ffa5"
    },
    "Microwave": {
        "power_on": (800, 1200),        # Heating
        "power_standby": (3, 6),        # Clock display
        "power_idle": (3, 6),           # Always showing clock
        "voltage": (220, 240),
        "typical_hours": {
            "morning": 0.3,   # 30% used (breakfast)
            "afternoon": 0.2, # 20% used (lunch)
            "evening": 0.5,   # 50% used (dinner)
            "night": 0.1      # 10% used (late snack)
        },
        "color": "#ff9f40"
    },
    "Air Conditioner": {
        "power_on": (1000, 1800),       # Cooling mode (1.5 ton AC)
        "power_standby": (10, 20),      # Fan only mode
        "power_idle": (2, 5),           # Remote standby
        "voltage": (220, 240),
        "typical_hours": {
            "morning": 0.1,   # 10% ON (cool mornings)
            "afternoon": 0.7, # 70% ON (hot afternoons)
            "evening": 0.5,   # 50% ON
            "night": 0.3      # 30% ON (sleeping hours)
        },
        "color": "#3498db"
    },
    "Laptop": {
        "power_on": (40, 80),           # Active use + charging
        "power_standby": (5, 15),       # Sleep mode
        "power_idle": (0.5, 2),         # Off but plugged
        "voltage": (220, 240),
        "typical_hours": {
            "morning": 0.6,   # 60% ON (work/study)
            "afternoon": 0.7, # 70% ON
            "evening": 0.5,   # 50% ON (entertainment)
            "night": 0.2      # 20% ON (late work)
        },
        "color": "#9b59b6"
    }
}

# ==================== AQI DATA CONFIGURATION ====================

# Based on real Indian AQI levels (New Delhi, Mumbai, Bangalore patterns)
AQI_PATTERNS = {
    "indoor": {
        "morning": (30, 70),    # Good to Moderate (windows closed)
        "afternoon": (40, 90),   # Moderate (cooking, activities)
        "evening": (50, 100),    # Moderate to Unhealthy (dinner cooking)
        "night": (25, 60)        # Good (settled down)
    },
    "outdoor": {
        "morning": (80, 180),    # Poor to Unhealthy (traffic rush)
        "afternoon": (60, 140),  # Moderate to Unhealthy
        "evening": (100, 220),   # Unhealthy to Very Unhealthy (peak pollution)
        "night": (70, 150)       # Moderate to Unhealthy
    }
}

# ==================== HELPER FUNCTIONS ====================

def get_time_of_day(hour):
    """Determine time of day category"""
    if 6 <= hour < 12:
        return "morning"
    elif 12 <= hour < 18:
        return "afternoon"
    elif 18 <= hour < 23:
        return "evening"
    else:
        return "night"

def get_device_mode(device_name, hour):
    """
    Determine realistic device mode based on time of day
    Returns: "ON", "Standby", or "Idle"
    """
    time_period = get_time_of_day(hour)
    device = DEVICES_CONFIG[device_name]
    
    # Get probability of device being ON
    on_probability = device["typical_hours"][time_period]
    
    # Random decision based on probability
    rand = random.random()
    
    if rand < on_probability:
        return "ON"
    elif rand < on_probability + 0.15:  # 15% chance of Standby
        return "Standby"
    else:
        return "Idle"

def generate_power_data(device_name, mode):
    """
    Generate realistic power consumption based on device and mode
    """
    device = DEVICES_CONFIG[device_name]
    
    if mode == "ON":
        power = random.uniform(*device["power_on"])
    elif mode == "Standby":
        power = random.uniform(*device["power_standby"])
    else:  # Idle
        power = random.uniform(*device["power_idle"])
    
    voltage = random.uniform(*device["voltage"])
    
    # Add realistic fluctuations (±5%)
    power *= random.uniform(0.95, 1.05)
    voltage *= random.uniform(0.98, 1.02)
    
    return round(power, 2), round(voltage, 2)

def generate_aqi_data(location_type, hour):
    """
    Generate realistic AQI values based on location and time
    """
    time_period = get_time_of_day(hour)
    aqi_range = AQI_PATTERNS[location_type][time_period]
    
    base_aqi = random.randint(*aqi_range)
    
    # Add some random variation (±10)
    aqi_value = base_aqi + random.randint(-10, 10)
    
    # Ensure within valid range
    aqi_value = max(0, min(500, aqi_value))
    
    return aqi_value

# ==================== DATA GENERATION FUNCTIONS ====================

def add_historical_electricity_data(days=7):
    """
    Generate realistic electricity data for past N days
    Simulates hourly readings for all devices
    """
    print(f"\n⚡ Generating {days} days of electricity data...")
    print("=" * 60)
    
    total_records = 0
    
    for day in range(days, 0, -1):
        print(f"\n📅 Day {days - day + 1}/{days} ({day} days ago)")
        
        for hour in range(24):
            timestamp = (datetime.now() - timedelta(days=day, hours=(24-hour))).isoformat()
            
            for device_name in DEVICES_CONFIG.keys():
                mode = get_device_mode(device_name, hour)
                power, voltage = generate_power_data(device_name, mode)
                
                data = {
                    "device_name": device_name,
                    "mode": mode,
                    "voltage": voltage,
                    "power_watts": power,
                    "timestamp": timestamp
                }
                
                try:
                    response = requests.post(f"{API_URL}/api/electricity/add", json=data)
                    if response.status_code == 201:
                        total_records += 1
                        if total_records % 50 == 0:
                            print(f"  ✓ {total_records} records added...")
                except Exception as e:
                    print(f"  ❌ Error: {e}")
                
                time.sleep(0.01)  # Small delay to avoid overwhelming server
    
    print(f"\n✅ Total electricity records added: {total_records}")
    return total_records

def add_historical_aqi_data(days=7):
    """
    Generate realistic AQI data for past N days
    Simulates hourly readings for indoor and outdoor
    """
    print(f"\n🌫️ Generating {days} days of AQI data...")
    print("=" * 60)
    
    total_records = 0
    
    for day in range(days, 0, -1):
        print(f"\n📅 Day {days - day + 1}/{days} ({day} days ago)")
        
        for hour in range(0, 24, 2):  # Every 2 hours
            timestamp = (datetime.now() - timedelta(days=day, hours=(24-hour))).isoformat()
            
            for location_type in ["indoor", "outdoor"]:
                aqi_value = generate_aqi_data(location_type, hour)
                
                data = {
                    "location_type": location_type,
                    "aqi_value": aqi_value,
                    "timestamp": timestamp
                }
                
                try:
                    response = requests.post(f"{API_URL}/api/aqi/add", json=data)
                    if response.status_code == 201:
                        total_records += 1
                except Exception as e:
                    print(f"  ❌ Error: {e}")
                
                time.sleep(0.01)
        
        print(f"  ✓ {24} AQI readings for day {days - day + 1}")
    
    print(f"\n✅ Total AQI records added: {total_records}")
    return total_records

def generate_realtime_simulation(duration_minutes=5):
    """
    Simulate real-time data for demo purposes
    Updates every 30 seconds for specified duration
    """
    print(f"\n🔴 LIVE SIMULATION MODE (Duration: {duration_minutes} minutes)")
    print("=" * 60)
    print("This will simulate real-time sensor updates for your demo")
    print("Press Ctrl+C to stop early\n")
    
    iterations = duration_minutes * 2  # Every 30 seconds
    
    try:
        for i in range(iterations):
            current_hour = datetime.now().hour
            print(f"\n⏱️  Update {i+1}/{iterations} - {datetime.now().strftime('%I:%M:%S %p')}")
            
            # Update electricity data for all devices
            for device_name in DEVICES_CONFIG.keys():
                mode = get_device_mode(device_name, current_hour)
                power, voltage = generate_power_data(device_name, mode)
                
                data = {
                    "device_name": device_name,
                    "mode": mode,
                    "voltage": voltage,
                    "power_watts": power,
                    "timestamp": datetime.now().isoformat()
                }
                
                response = requests.post(f"{API_URL}/api/electricity/add", json=data)
                if response.status_code == 201:
                    print(f"  ⚡ {device_name}: {power}W ({mode})")
            
            # Update AQI data
            for location_type in ["indoor", "outdoor"]:
                aqi_value = generate_aqi_data(location_type, current_hour)
                
                data = {
                    "location_type": location_type,
                    "aqi_value": aqi_value,
                    "timestamp": datetime.now().isoformat()
                }
                
                response = requests.post(f"{API_URL}/api/aqi/add", json=data)
                if response.status_code == 201:
                    print(f"  🌫️  {location_type.capitalize()} AQI: {aqi_value}")
            
            if i < iterations - 1:
                print(f"\n  ⏳ Waiting 30 seconds...")
                time.sleep(30)
    
    except KeyboardInterrupt:
        print("\n\n🛑 Simulation stopped by user")

def display_statistics():
    """
    Display current database statistics
    """
    print("\n📊 DATABASE STATISTICS")
    print("=" * 60)
    
    try:
        response = requests.get(f"{API_URL}/api/stats")
        if response.status_code == 200:
            stats = response.json()['data']
            
            print(f"  Total AQI Records: {stats['total_aqi_records']}")
            print(f"  Total Electricity Records: {stats['total_electricity_records']}")
            print(f"  Monitored Devices: {stats['device_count']}")
            print(f"  Device List: {', '.join(stats['monitored_devices'])}")
            
            # Calculate expected daily cost
            print(f"\n💰 ESTIMATED DAILY COST")
            total_records = stats['total_electricity_records']
            if total_records > 0:
                elec_response = requests.get(f"{API_URL}/api/electricity/history?limit=100")
                if elec_response.status_code == 200:
                    data = elec_response.json()['data']
                    avg_power = sum(d['power_watts'] for d in data) / len(data)
                    daily_kwh = (avg_power / 1000) * 24
                    daily_cost = daily_kwh * 7  # ₹7 per kWh (India average)
                    monthly_cost = daily_cost * 30
                    
                    print(f"  Average Power: {avg_power:.2f} W")
                    print(f"  Daily Usage: {daily_kwh:.2f} kWh")
                    print(f"  Daily Cost: ₹{daily_cost:.2f}")
                    print(f"  Monthly Cost: ₹{monthly_cost:.2f}")
        else:
            print("  ❌ Could not fetch statistics")
    
    except Exception as e:
        print(f"  ❌ Error: {e}")

# ==================== MAIN MENU ====================

def main():
    """
    Interactive menu for data generation
    """
    print("\n" + "=" * 60)
    print("  🌍 ECOTRACK - ADVANCED TEST DATA GENERATOR")
    print("=" * 60)
    
    # Check if backend is running
    try:
        response = requests.get(f"{API_URL}/")
        if response.status_code != 200:
            print("\n❌ Error: Backend is not responding correctly!")
            print("Please start the backend first: python app.py")
            return
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Cannot connect to backend server!")
        print("Please start the backend first: python app.py")
        return
    
    print("\n✅ Backend server connected successfully!")
    
    while True:
        print("\n" + "=" * 60)
        print("SELECT DATA GENERATION MODE:")
        print("=" * 60)
        print("  1. Quick Demo Data (Last 24 hours)")
        print("  2. Weekly Data (7 days)")
        print("  3. Monthly Data (30 days)")
        print("  4. Real-time Simulation (for live demo)")
        print("  5. View Database Statistics")
        print("  6. Exit")
        print("=" * 60)
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == "1":
            print("\n🚀 Generating 24 hours of demo data...")
            electricity_count = add_historical_electricity_data(days=1)
            aqi_count = add_historical_aqi_data(days=1)
            print(f"\n✅ COMPLETE! Total records: {electricity_count + aqi_count}")
            display_statistics()
            
        elif choice == "2":
            print("\n🚀 Generating 7 days of data...")
            electricity_count = add_historical_electricity_data(days=7)
            aqi_count = add_historical_aqi_data(days=7)
            print(f"\n✅ COMPLETE! Total records: {electricity_count + aqi_count}")
            display_statistics()
            
        elif choice == "3":
            confirm = input("\n⚠️  This will generate ~57,600 records. Continue? (yes/no): ")
            if confirm.lower() == "yes":
                print("\n🚀 Generating 30 days of data (this may take 10-15 minutes)...")
                electricity_count = add_historical_electricity_data(days=30)
                aqi_count = add_historical_aqi_data(days=30)
                print(f"\n✅ COMPLETE! Total records: {electricity_count + aqi_count}")
                display_statistics()
            
        elif choice == "4":
            duration = input("\nEnter simulation duration in minutes (default: 5): ").strip()
            duration = int(duration) if duration.isdigit() else 5
            generate_realtime_simulation(duration_minutes=duration)
            
        elif choice == "5":
            display_statistics()
            
        elif choice == "6":
            print("\n👋 Exiting... Thank you for using EcoTrack!")
            break
        
        else:
            print("\n❌ Invalid choice! Please enter 1-6")

if __name__ == "__main__":
    main()
