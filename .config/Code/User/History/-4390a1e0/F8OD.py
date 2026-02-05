from tuya_connector import TuyaOpenAPI
import time
import sys

ACCESS_ID = "YOUR_ACCESS_ID"
ACCESS_SECRET = "YOUR_ACCESS_SECRET"
DEVICE_ID = "YOUR_DEVICE_ID"

ENDPOINT = "https://openapi.tuya.com"  # global (most stable)

def connect():
    try:
        api = TuyaOpenAPI(ENDPOINT, ACCESS_ID, ACCESS_SECRET)
        api.connect()
        print("✅ Connected to Tuya Cloud")
        return api
    except Exception as e:
        print("❌ Failed to connect to Tuya Cloud")
        print(e)
        sys.exit(1)

def send(api, value):
    res = api.post(
        f"/v1.0/iot-03/devices/{DEVICE_ID}/commands",
        {"commands": [{"code": "switch_1", "value": value}]}
    )

    if not res or not res.get("success"):
        print("❌ Command failed:", res)
    else:
        print("✅ Plug", "ON" if value else "OFF")

def main():
    api = connect()

    while True:
        print("\n1. Turn ON")
        print("2. Turn OFF")
        print("3. Exit")

        ch = input("Choice: ")

        if ch == "1":
            send(api, True)
        elif ch == "2":
            send(api, False)
        elif ch == "3":
            break
        else:
            print("Invalid choice")

        time.sleep(1)

if __name__ == "__main__":
    main()
