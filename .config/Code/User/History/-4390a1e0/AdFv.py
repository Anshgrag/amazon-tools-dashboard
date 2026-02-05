from tuya_connector import TuyaOpenAPI
import time

# ============================
# 🔴 FILL THESE VALUES
# ============================
ACCESS_ID = "m3negp3fvw7ugp7cqae8"
ACCESS_SECRET = "45b5bc2934f7437bb52739090eb96c5c"
DEVICE_ID = "d78fcea6e6c3b03d40zcwp"

ENDPOINT = "https://openapi.tuya.in"  # India data center
# ============================

def connect():
    api = TuyaOpenAPI(ENDPOINT, ACCESS_ID, ACCESS_SECRET)
    api.connect()
    return api

def turn_on(api):
    api.post(f"/v1.0/iot-03/devices/{DEVICE_ID}/commands", {
        "commands": [{"code": "switch_1", "value": True}]
    })
    print("✅ Plug turned ON")

def turn_off(api):
    api.post(f"/v1.0/iot-03/devices/{DEVICE_ID}/commands", {
        "commands": [{"code": "switch_1", "value": False}]
    })
    print("❌ Plug turned OFF")

def menu():
    print("\n===== WIPRO SMART PLUG (CLOUD) =====")
    print("1. Turn ON")
    print("2. Turn OFF")
    print("3. Exit")

def main():
    api = connect()

    while True:
        menu()
        ch = input("Enter choice: ")

        if ch == "1":
            turn_on(api)
        elif ch == "2":
            turn_off(api)
        elif ch == "3":
            print("Bye 👋")
            break
        else:
            print("Invalid choice")

        time.sleep(1)

if __name__ == "__main__":
    main()
