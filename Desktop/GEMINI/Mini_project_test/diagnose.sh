#!/bin/bash

echo "🔍 COMPREHENSIVE ERROR CHECKING"
echo "=================================="

echo -e "\n📊 1. Backend API Status:"
if curl -s http://localhost:5000 >/dev/null 2>&1; then
    echo "✅ Backend is running on port 5000"
    curl -s http://localhost:5000 | jq -r .message
else
    echo "❌ Backend is NOT running"
    echo "Start with: cd backend && source venv/bin/activate && python app.py"
fi

echo -e "\n🌐 2. Frontend Status:"
if curl -s http://localhost:8000 >/dev/null 2>&1; then
    echo "✅ Frontend is running on port 8000"
else
    echo "❌ Frontend is NOT running"
    echo "Start with: cd frontend && python3 -m http.server 8000"
fi

echo -e "\n📈 3. API Endpoints Testing:"
echo "----------------------------------------"

# Test savings endpoint
echo -n "💰 Savings API: "
SAVINGS_RESPONSE=$(curl -s http://localhost:5000/api/savings 2>/dev/null)
if echo "$SAVINGS_RESPONSE" | jq -e .status >/dev/null 2>&1; then
    STATUS=$(echo "$SAVINGS_RESPONSE" | jq -r .status)
    if [ "$STATUS" = "success" ]; then
        echo "✅ Working"
        WASTE=$(echo "$SAVINGS_RESPONSE" | jq -r .data.total_waste_cost)
        SAVED=$(echo "$SAVINGS_RESPONSE" | jq -r .data.total_saved_cost)
        echo "   📊 Waste: \$$WASTE, Saved: \$$SAVED"
    else
        echo "❌ API Error: $(echo "$SAVINGS_RESPONSE" | jq -r .message)"
    fi
else
    echo "❌ No response or invalid JSON"
fi

# Test electricity endpoint
echo -n "⚡ Electricity API: "
if curl -s http://localhost:5000/api/electricity/history?limit=1 | jq -e .status >/dev/null 2>&1; then
    echo "✅ Working"
    COUNT=$(curl -s http://localhost:5000/api/electricity/history?limit=1 | jq -r .count)
    echo "   📊 Records: $COUNT"
else
    echo "❌ Not working"
fi

echo -e "\n📋 4. Database Status:"
echo "----------------------------------------"
if [ -f "/home/bot4u/Desktop/GEMINI/Mini_project/backend/ecotrack.db" ]; then
    echo "✅ Database file exists"
    
    # Check if database has data
    CD_COUNT=$(sqlite3 /home/bot4u/Desktop/GEMINI/Mini_project/backend/ecotrack.db "SELECT COUNT(*) FROM electricity_data;" 2>/dev/null || echo "0")
    echo "📊 Electricity records: $CD_COUNT"
    
    if [ "$CD_COUNT" -gt 0 ]; then
        echo "✅ Database has data"
        
        # Check for auto_controlled column
        if sqlite3 /home/bot4u/Desktop/GEMINI/Mini_project/backend/ecotrack.db "PRAGMA table_info(electricity_data);" | grep -q auto_controlled; then
            echo "✅ Database schema is up to date"
        else
            echo "❌ Database schema needs update - run with fresh database"
        fi
    else
        echo "⚠️  Database is empty - run test data generator"
        echo "   Command: cd backend && source venv/bin/activate && python savings_test_data.py"
    fi
else
    echo "❌ Database file not found - will be created when backend starts"
fi

echo -e "\n🎨 5. Frontend Files:"
echo "----------------------------------------"
cd /home/bot4u/Desktop/GEMINI/Mini_project/frontend

if [ -f "index.html" ]; then
    echo "✅ index.html exists"
    
    if grep -q "savingsChart" index.html; then
        echo "✅ Savings chart element found"
    else
        echo "❌ Savings chart element missing"
    fi
    
    if grep -q "deviceSavingsList" index.html; then
        echo "✅ Device savings list element found"
    else
        echo "❌ Device savings list element missing"
    fi
else
    echo "❌ index.html not found"
fi

if [ -f "script.js" ]; then
    echo "✅ script.js exists"
    
    if grep -q "updateSavingsDisplay" script.js; then
        echo "✅ updateSavingsDisplay function found"
    else
        echo "❌ updateSavingsDisplay function missing"
    fi
    
    if grep -q "createSavingsChart" script.js; then
        echo "✅ createSavingsChart function found"
    else
        echo "❌ createSavingsChart function missing"
    fi
    
    if grep -q "fetchSavingsData" script.js; then
        echo "✅ fetchSavingsData function found"
    else
        echo "❌ fetchSavingsData function missing"
    fi
else
    echo "❌ script.js not found"
fi

if [ -f "style.css" ]; then
    echo "✅ style.css exists"
    
    if grep -q "savings-summary" style.css; then
        echo "✅ Savings styles found"
    else
        echo "❌ Savings styles missing"
    fi
else
    echo "❌ style.css not found"
fi

echo -e "\n🚀 6. Quick Fix Commands:"
echo "----------------------------------------"
echo "If any errors above, run these commands:"
echo ""
echo "# Start backend:"
echo "cd /home/bot4u/Desktop/GEMINI/Mini_project/backend"
echo "source venv/bin/activate"
echo "python app.py"
echo ""
echo "# Start frontend:"
echo "cd /home/bot4u/Desktop/GEMINI/Mini_project/frontend"
echo "python3 -m http.server 8000"
echo ""
echo "# Generate test data:"
echo "cd /home/bot4u/Desktop/GEMINI/Mini_project/backend"
echo "source venv/bin/activate"
echo "python savings_test_data.py"
echo ""
echo "# View dashboard:"
echo "Open http://localhost:8000 in browser"

echo -e "\n🎯 CHECK COMPLETE!"
echo "Open browser console (F12) to see any JavaScript errors"