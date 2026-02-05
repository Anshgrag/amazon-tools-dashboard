import tinytuya
import time

DEVICE_ID = "d78fcea6e6c3b03d40zcwp"
IP = "192.168.1.43"
LOCAL_KEY = "YOUR_LOCAL_KEY"

device = tinytuya.OutletDevice(
    DEVICE_ID,
    IP,
    LOCAL_KEY,
    version=3.3
)

device.set_socketPersistent(True)

print("🔌 Live Power Monitoring (Local LAN)")
print("===================================")

while True:
    data = device.status()["dps"]

    power = data.get("24", 0) / 10      # Watts
    voltage = data.get("23", 0) / 100   # Volts
    current = data.get("20", 0) / 1000  # Amps

    print(f"Voltage: {voltage:.2f} V | Current: {current:.3f} A | Power: {power:.2f} W")

    time.sleep(2)
