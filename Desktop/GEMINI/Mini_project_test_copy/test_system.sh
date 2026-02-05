#!/bin/bash

echo "=== COMPREHENSIVE ECO TRACK TEST ==="

echo "1. Testing Backend APIs..."
echo "   Devices API: $(curl -s http://localhost:5000/api/devices | python3 -c 'import json,sys; data=json.load(sys.stdin); print("✅" if data["status"]=="success" else "❌")')"
echo "   Savings API: $(curl -s http://localhost:5000/api/savings?period=month | python3 -c 'import json,sys; data=json.load(sys.stdin); print("✅" if data["status"]=="success" else "❌")')"
echo "   Electricity API: $(curl -s http://localhost:5000/api/electricity/history?period=month | python3 -c 'import json,sys; data=json.load(sys.stdin); print("✅" if data["status"]=="success" else "❌")')"
echo "   Rooms API: $(curl -s http://localhost:5000/api/rooms/usage?period=month | python3 -c 'import json,sys; data=json.load(sys.stdin); print("✅" if data["status"]=="success" else "❌")')"

echo ""
echo "2. Testing Frontend..."
echo "   Frontend Server: $(curl -s http://localhost:8000 > /dev/null && echo "✅" || echo "❌")"

echo ""
echo "3. Checking Processes..."
echo "   Backend Process: $(pgrep -f 'python3 app.py' > /dev/null && echo "✅ Running" || echo "❌ Stopped")"
echo "   Frontend Process: $(pgrep -f 'python3 -m http.server' > /dev/null && echo "✅ Running" || echo "❌ Stopped")"

echo ""
echo "4. Testing Data Flow..."
DEVICES=$(curl -s http://localhost:5000/api/devices | python3 -c 'import json,sys; data=json.load(sys.stdin); print(len(data["data"]["devices"]))')
echo "   Available Devices: $DEVICES"

if [ "$DEVICES" -gt 0 ]; then
    echo "   Data Status: ✅ Has device data"
else
    echo "   Data Status: ⚠️  No device data found"
fi

echo ""
echo "5. Instructions for Manual Testing:"
echo "   1. Open browser and go to: http://localhost:8000"
echo "   2. Open browser console (F12) to see debug messages"
echo "   3. Click on each tab: Dashboard, Cost, Appliances, Usage by Rooms"
echo "   4. Click on time filters: Today, Month, Year"
echo "   5. Check console for any JavaScript errors"

echo ""
echo "=== END TEST ==="