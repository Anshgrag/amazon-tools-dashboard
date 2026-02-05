// ==================== CONFIGURATION ====================

const API_BASE_URL = 'http://localhost:5000';
const REFRESH_INTERVAL = 30000;

let costChart = null;
let usageChart = null;
let aqiGauge = null;

// ==================== UTILITY FUNCTIONS ====================

function formatCurrency(value) {
    return `$${value.toFixed(0)}`;
}

function formatDate() {
    const now = new Date();
    const options = { month: 'long', year: 'numeric' };
    return now.toLocaleDateString('en-US', options);
}

function getAQICategory(aqiValue) {
    if (aqiValue <= 50) return { category: 'Good', color: '#06ffa5' };
    else if (aqiValue <= 100) return { category: 'Moderate', color: '#ffd166' };
    else if (aqiValue <= 150) return { category: 'Unhealthy for Sensitive', color: '#ff9f40' };
    else if (aqiValue <= 200) return { category: 'Unhealthy', color: '#ff6b9d' };
    else if (aqiValue <= 300) return { category: 'Very Unhealthy', color: '#c77dff' };
    else return { category: 'Hazardous', color: '#ff4757' };
}

// ==================== FETCH DATA FUNCTIONS ====================

async function fetchLatestAQI() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/aqi/latest`);
        const result = await response.json();
        
        if (result.status === 'success') {
            updateAQIDisplay(result.data);
        }
    } catch (error) {
        console.error('Error fetching AQI data:', error);
    }
}

async function fetchElectricityData() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/electricity/history?limit=100`);
        const result = await response.json();
        
        if (result.status === 'success') {
            updateAppliancesDisplay(result.data);
            updateCostPredicted(result.data);
            updateUsageEstimate(result.data);
            updateCarbonFootprint(result.data);
        }
    } catch (error) {
        console.error('Error fetching electricity data:', error);
    }
}

// ==================== UPDATE DISPLAY FUNCTIONS ====================

function updateAQIDisplay(data) {
    let avgAQI = 0;
    let count = 0;
    
    if (data.indoor) {
        document.getElementById('indoorAQI').textContent = data.indoor.aqi_value;
        avgAQI += data.indoor.aqi_value;
        count++;
    }
    
    if (data.outdoor) {
        document.getElementById('outdoorAQI').textContent = data.outdoor.aqi_value;
        avgAQI += data.outdoor.aqi_value;
        count++;
    }
    
    if (count > 0) {
        avgAQI = Math.round(avgAQI / count);
        document.getElementById('aqiValue').textContent = avgAQI;
        createAQIGauge(avgAQI);
    }
}

function updateAppliancesDisplay(data) {
    const appliancesList = document.getElementById('appliancesList');
    
    // Get latest reading for each device
    const deviceMap = {};
    data.forEach(record => {
        if (!deviceMap[record.device_name] || 
            new Date(record.timestamp) > new Date(deviceMap[record.device_name].timestamp)) {
            deviceMap[record.device_name] = record;
        }
    });
    
    // Define colors for each appliance
    const colors = {
        'TV': '#ff6b9d',
        'Router': '#c77dff',
        'Charger': '#4ecdc4',
        'Refrigerator': '#ffd166'
    };
    
    // Sort by power consumption
    const devices = Object.values(deviceMap).sort((a, b) => b.power_watts - a.power_watts);
    
    let html = '';
    devices.forEach(device => {
        const maxPower = 200; // Maximum power for bar width calculation
        const barWidth = Math.min((device.power_watts / maxPower) * 100, 100);
        const color = colors[device.device_name] || '#4ecdc4';
        
        html += `
            <div class="appliance-item">
                <div class="appliance-name">${device.device_name}</div>
                <div class="appliance-bar">
                    <div class="appliance-bar-fill" style="width: ${barWidth}%; background: ${color};"></div>
                </div>
                <div class="appliance-value">${device.power_watts.toFixed(1)} kWh</div>
            </div>
        `;
    });
    
    appliancesList.innerHTML = html;
}

function updateCostPredicted(data) {
    // Calculate total power consumption
    let totalPower = 0;
    data.forEach(record => {
        totalPower += record.power_watts;
    });
    
    // Estimate cost (assuming $0.12 per kWh)
    const avgPowerKW = totalPower / data.length / 1000;
    const hoursPerMonth = 730;
    const costPerKWh = 0.12;
    const totalCost = avgPowerKW * hoursPerMonth * costPerKWh;
    
    // Split between electricity (80%) and gas (20%)
    const electricityCost = totalCost * 0.8;
    const gasCost = totalCost * 0.2;
    
    document.getElementById('totalCost').textContent = formatCurrency(totalCost);
    
    // Update cost comparison
    const lastMonthCost = totalCost * 0.95; // Simulate last month (5% less)
    const changePercent = ((totalCost - lastMonthCost) / lastMonthCost * 100).toFixed(2);
    
    document.getElementById('lastMonthValue').textContent = formatCurrency(lastMonthCost);
    document.getElementById('currentMonthValue').textContent = formatCurrency(totalCost);
    document.getElementById('changePercentage').textContent = `${changePercent}%`;
    
    createCostChart(electricityCost, gasCost);
}

function updateUsageEstimate(data) {
    // Calculate usage
    let totalPower = 0;
    data.forEach(record => {
        totalPower += record.power_watts;
    });
    
    const avgPowerKW = totalPower / data.length / 1000;
    const currentDay = new Date().getDate();
    const daysInMonth = 30;
    
    const usageTillNow = avgPowerKW * currentDay * 24;
    const usagePredicted = avgPowerKW * daysInMonth * 24;
    
    document.getElementById('usageTillNow').textContent = `${usageTillNow.toFixed(1)} kWh`;
    document.getElementById('usagePredicted').textContent = `${usagePredicted.toFixed(1)} kWh`;
    
    createUsageChart(usageTillNow, usagePredicted);
}

function updateCarbonFootprint(data) {
    // Calculate emissions (0.92 lbs CO2 per kWh = 0.417 kg CO2 per kWh)
    let totalPower = 0;
    data.forEach(record => {
        totalPower += record.power_watts;
    });
    
    const avgPowerKW = totalPower / data.length / 1000;
    const currentDay = new Date().getDate();
    const daysInMonth = 30;
    
    const usageTillNow = avgPowerKW * currentDay * 24;
    const usagePredicted = avgPowerKW * daysInMonth * 24;
    
    const emissionTillDate = usageTillNow * 0.417;
    const emissionPredicted = usagePredicted * 0.417;
    
    document.getElementById('emissionTillDate').textContent = `${emissionTillDate.toFixed(1)} Kg of CO2`;
    document.getElementById('emissionPredicted').textContent = `${emissionPredicted.toFixed(1)} Kg of CO2`;
    
    // Green energy (simulate 30% of usage)
    const greenEnergy = usageTillNow * 0.3;
    const greenGoal = 500;
    const greenPercent = Math.min((greenEnergy / greenGoal) * 100, 100);
    
    document.getElementById('greenCurrent').textContent = `${greenEnergy.toFixed(0)} kWh`;
    document.getElementById('greenProgress').style.width = `${greenPercent}%`;
}

// ==================== CHART FUNCTIONS ====================

function createCostChart(electricityCost, gasCost) {
    const ctx = document.getElementById('costChart');
    if (!ctx) return;
    
    if (costChart) {
        costChart.destroy();
    }
    
    costChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Electricity', 'Gas'],
            datasets: [{
                data: [electricityCost, gasCost],
                backgroundColor: ['#4ecdc4', '#ffd166'],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '75%',
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return context.label + ': $' + context.parsed.toFixed(2);
                        }
                    }
                }
            }
        }
    });
}

function createUsageChart(tillNow, predicted) {
    const ctx = document.getElementById('usageChart');
    if (!ctx) return;
    
    if (usageChart) {
        usageChart.destroy();
    }
    
    // Generate data for the month
    const currentDay = new Date().getDate();
    const labels = [];
    const data = [];
    
    for (let i = 1; i <= 30; i++) {
        labels.push(`Jun ${i}`);
        if (i <= currentDay) {
            data.push((tillNow / currentDay) * i);
        } else {
            data.push(null);
        }
    }
    
    usageChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                borderColor: '#ff6b9d',
                backgroundColor: 'rgba(255, 107, 157, 0.1)',
                fill: true,
                tension: 0.4,
                pointRadius: 4,
                pointBackgroundColor: '#ff6b9d',
                pointBorderColor: '#fff',
                pointBorderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                x: {
                    display: true,
                    grid: {
                        color: 'rgba(255, 255, 255, 0.05)'
                    },
                    ticks: {
                        color: '#b0c4de',
                        maxRotation: 0,
                        autoSkip: true,
                        maxTicksLimit: 6
                    }
                },
                y: {
                    display: true,
                    grid: {
                        color: 'rgba(255, 255, 255, 0.05)'
                    },
                    ticks: {
                        color: '#b0c4de'
                    }
                }
            }
        }
    });
}

function createAQIGauge(aqiValue) {
    const ctx = document.getElementById('aqiGauge');
    if (!ctx) return;
    
    if (aqiGauge) {
        aqiGauge.destroy();
    }
    
    const aqiInfo = getAQICategory(aqiValue);
    const maxAQI = 500;
    const percentage = (aqiValue / maxAQI) * 100;
    
    aqiGauge = new Chart(ctx, {
        type: 'doughnut',
        data: {
            datasets: [{
                data: [percentage, 100 - percentage],
                backgroundColor: [aqiInfo.color, 'rgba(255, 255, 255, 0.1)'],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '75%',
            rotation: -90,
            circumference: 180,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    enabled: false
                }
            }
        }
    });
}

// ==================== INITIALIZATION ====================

async function refreshDashboard() {
    console.log('Refreshing dashboard...');
    document.getElementById('currentDate').textContent = formatDate();
    
    await Promise.all([
        fetchLatestAQI(),
        fetchElectricityData()
    ]);
}

window.addEventListener('DOMContentLoaded', () => {
    console.log('EcoTrack Dashboard Initialized');
    refreshDashboard();
    setInterval(refreshDashboard, REFRESH_INTERVAL);
});
