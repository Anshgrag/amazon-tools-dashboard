#!/bin/bash
echo "=== Testing API Endpoints ==="
echo "1. Backend Status:"
curl -s http://localhost:5000 | jq .message

echo -e "\n2. Savings API:"
curl -s http://localhost:5000/api/savings | jq .status

echo -e "\n3. Electricity API:"
curl -s http://localhost:5000/api/electricity/history?limit=1 | jq .count

echo -e "\n4. Frontend Status:"
curl -s -o /dev/null -w "%{http_code}" http://localhost:8000

echo -e "\n5. Chart.js CDN:"
curl -s -o /dev/null -w "%{http_code}" https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js

echo -e "\n=== Checking for JavaScript Errors ==="
echo "Open browser console and check for errors"
echo "Visit: http://localhost:8000"