// ==================== CONFIGURATION ====================

const API_BASE_URL = 'http://localhost:5000';
const REFRESH_INTERVAL = 30000;
let currentPeriod = 'month'; // Default period

let costChart = null;
let usageChart = null;
let savingsChart = null;

// ==================== UTILITY FUNCTIONS ====================

function formatCurrency(value) {
    return `$${parseFloat(value).toFixed(2)}`;
}

function formatDate() {
    const now = new Date();
    const options = { month: 'long', year: 'numeric' };
    return now.toLocaleDateString('en-US', options);
}

// ==================== FETCH DATA FUNCTIONS ====================

async function fetchElectricityData() {
    try {
        console.log('Fetching electricity data for period:', currentPeriod);
        const response = await fetch(`${API_BASE_URL}/api/electricity/history?period=${currentPeriod}`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        console.log('Electricity data received:', result);
        
        if (result.status === 'success') {
            updateAppliancesDisplay(result.data);
            updateCostPredicted(result.data);
            updateUsageEstimate(result.data);
            updateCarbonFootprint(result.data);
        } else {
            console.error('API returned error:', result);
        }
    } catch (error) {
        console.error('Error fetching electricity data:', error);
    }
}

async function fetchSavingsData() {
    try {
        console.log('=== FETCHING SAVINGS DATA FOR PERIOD:', currentPeriod);
        const response = await fetch(`${API_BASE_URL}/api/savings?period=${currentPeriod}`);
        
        console.log('Response status:', response.status);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        console.log('Savings data received:', result);
        
        if (result.status === 'success') {
            console.log('Calling updateSavingsDisplay with data:', result.data);
            updateSavingsDisplay(result.data);
        } else {
            console.error('API returned error:', result);
        }
    } catch (error) {
        console.error('Error fetching savings data:', error);
    }
}

// ==================== UPDATE DISPLAY FUNCTIONS ====================

function updateAppliancesDisplay(data) {
    const appliancesList = document.getElementById('appliancesList');
    if (!appliancesList) return;
    
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
        const maxPower = 200;
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
    
    const totalCostElement = document.getElementById('totalCost');
    if (totalCostElement) totalCostElement.textContent = formatCurrency(totalCost);
    
    // Update cost comparison
    const lastMonthCost = totalCost * 0.95;
    const changePercent = ((totalCost - lastMonthCost) / lastMonthCost * 100).toFixed(2);
    
    const lastMonthElement = document.getElementById('lastMonthValue');
    const currentMonthElement = document.getElementById('currentMonthValue');
    const changeElement = document.getElementById('changePercentage');
    
    if (lastMonthElement) lastMonthElement.textContent = formatCurrency(lastMonthCost);
    if (currentMonthElement) currentMonthElement.textContent = formatCurrency(totalCost);
    if (changeElement) changeElement.textContent = `${changePercent}%`;
    
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
    
    const usageTillElement = document.getElementById('usageTillNow');
    const usagePredElement = document.getElementById('usagePredicted');
    
    if (usageTillElement) usageTillElement.textContent = `${usageTillNow.toFixed(1)} kWh`;
    if (usagePredElement) usagePredElement.textContent = `${usagePredicted.toFixed(1)} kWh`;
    
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
    
    const emissionTillElement = document.getElementById('emissionTillDate');
    const emissionPredElement = document.getElementById('emissionPredicted');
    
    if (emissionTillElement) emissionTillElement.textContent = `${emissionTillDate.toFixed(1)} Kg of CO2`;
    if (emissionPredElement) emissionPredElement.textContent = `${emissionPredicted.toFixed(1)} Kg of CO2`;
    
    // Green energy (simulate 30% of usage)
    const greenEnergy = usageTillNow * 0.3;
    const greenGoal = 500;
    const greenPercent = Math.min((greenEnergy / greenGoal) * 100, 100);
    
    const greenCurrentElement = document.getElementById('greenCurrent');
    const greenProgressElement = document.getElementById('greenProgress');
    
    if (greenCurrentElement) greenCurrentElement.textContent = `${greenEnergy.toFixed(0)} kWh`;
    if (greenProgressElement) greenProgressElement.style.width = `${greenPercent}%`;
}

// ==================== SAVINGS UPDATE FUNCTIONS ====================

function updateSavingsDisplay(data) {
    console.log('=== UPDATING SAVINGS DISPLAY ===');
    console.log('Data received:', data);
    
    try {
        // Get elements with null checks
        const wastedAmount = document.getElementById('wastedAmount');
        const savedAmount = document.getElementById('savedAmount');
        const netSavings = document.getElementById('netSavings');
        const savingsPercentage = document.getElementById('savingsPercentage');
        
        console.log('Elements found:');
        console.log('wastedAmount:', !!wastedAmount);
        console.log('savedAmount:', !!savedAmount);
        console.log('netSavings:', !!netSavings);
        console.log('savingsPercentage:', !!savingsPercentage);
        
        if (!wastedAmount || !savedAmount || !netSavings || !savingsPercentage) {
            console.error('Savings display elements not found');
            return;
        }
        
        // Extract values with defaults
        const totalWaste = parseFloat(data.total_waste_cost) || 0;
        const totalSaved = parseFloat(data.total_saved_cost) || 0;
        const netSavingsValue = parseFloat(data.net_savings) || 0;
        
        console.log('Parsed values:');
        console.log('totalWaste:', totalWaste);
        console.log('totalSaved:', totalSaved);
        console.log('netSavingsValue:', netSavingsValue);
        
        // Format currency values
        const wasteFormatted = formatCurrency(totalWaste);
        const savedFormatted = formatCurrency(totalSaved);
        const netFormatted = formatCurrency(netSavingsValue);
        
        console.log('Formatted values:');
        console.log('wasteFormatted:', wasteFormatted);
        console.log('savedFormatted:', savedFormatted);
        console.log('netFormatted:', netFormatted);
        
        // Update main savings amounts
        wastedAmount.textContent = wasteFormatted;
        savedAmount.textContent = savedFormatted;
        netSavings.textContent = netFormatted;
        
        console.log('Updated amounts successfully');
        
        // Calculate and update percentage
        const totalPotential = totalWaste + totalSaved;
        const percentage = totalPotential > 0 ? (totalSaved / totalPotential * 100) : 0;
        savingsPercentage.textContent = `${percentage.toFixed(1)}%`;
        
        console.log('Updated percentage:', percentage.toFixed(1) + '%');
        
        // Update device savings list
        if (data.device_details && Array.isArray(data.device_details)) {
            console.log('Updating device list with:', data.device_details);
            updateDeviceSavingsList(data.device_details);
        }
        
        // Create savings chart
        console.log('Creating chart with values:', totalWaste, totalSaved);
        createSavingsChart(totalWaste, totalSaved);
        
        console.log('=== SAVINGS DISPLAY UPDATED ===');
        
    } catch (error) {
        console.error('Error updating savings display:', error);
        console.error('Stack trace:', error.stack);
    }
}

function updateDeviceSavingsList(devices) {
    const deviceSavingsList = document.getElementById('deviceSavingsList');
    if (!deviceSavingsList) return;
    
    if (!devices || devices.length === 0) {
        deviceSavingsList.innerHTML = '<div class="no-devices">No device data available</div>';
        return;
    }
    
    let html = '';
    devices.forEach(device => {
        const netSaving = (device.saved_cost || 0) - (device.waste_cost || 0);
        const isPositive = netSaving >= 0;
        
        html += `
            <div class="device-savings-item">
                <div class="device-info">
                    <div class="device-name">${device.device_name || 'Unknown Device'}</div>
                    <div class="device-power">
                        <span class="waste-power">-${(device.waste_power || 0).toFixed(1)}W</span>
                        <span class="saved-power">+${(device.saved_power || 0).toFixed(1)}W</span>
                    </div>
                </div>
                <div class="device-savings ${isPositive ? 'positive' : 'negative'}">
                    ${isPositive ? '+' : ''}${formatCurrency(netSaving)}
                </div>
            </div>
        `;
    });
    
    deviceSavingsList.innerHTML = html;
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

function createSavingsChart(wasteCost, savedCost) {
    console.log('=== CREATING SAVINGS CHART ===');
    console.log('Values:', wasteCost, savedCost);
    
    try {
        const ctx = document.getElementById('savingsChart');
        if (!ctx) {
            console.error('Savings chart canvas not found');
            return;
        }
        
        if (savingsChart) {
            savingsChart.destroy();
        }
        
        // Ensure we have valid numbers
        const waste = Math.max(0, wasteCost || 0);
        const saved = Math.max(0, savedCost || 0);
        
        console.log('Creating chart with:', { waste, saved });
        
        savingsChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Without Automation', 'With Automation'],
                datasets: [{
                    data: [waste, saved],
                    backgroundColor: ['#ff6b9d', '#06ffa5'],
                    borderRadius: 8,
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return context.label + ': $' + context.parsed.y.toFixed(2);
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        display: true,
                        grid: {
                            display: false
                        },
                        ticks: {
                            color: '#b0c4de',
                            font: {
                                size: 11
                            }
                        }
                    },
                    y: {
                        display: true,
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(255, 255, 255, 0.05)'
                        },
                        ticks: {
                            color: '#b0c4de',
                            callback: function(value) {
                                return '$' + value;
                            }
                        }
                    }
                }
            }
        });
        
        console.log('=== SAVINGS CHART CREATED ===');
        
    } catch (error) {
        console.error('Error creating savings chart:', error);
    }
}

// ==================== TIME FILTER FUNCTIONS ====================

function setupTimeFilters() {
    const filterButtons = document.querySelectorAll('.filter-btn');
    
    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            const selectedPeriod = this.textContent.toLowerCase();
            
            // Don't do anything if clicking the already active button
            if (selectedPeriod === currentPeriod) {
                console.log('Already selected period:', selectedPeriod);
                return;
            }
            
            console.log('Switching to period:', selectedPeriod);
            
            // Remove active class from all buttons
            filterButtons.forEach(btn => btn.classList.remove('active'));
            
            // Add active class to clicked button
            this.classList.add('active');
            
            // Update current period
            currentPeriod = selectedPeriod;
            
            // Update date display
            updateDateDisplay(selectedPeriod);
            
            // Refresh dashboard with new period
            refreshDashboard();
        });
    });
}

function updateDateDisplay(period) {
    const dateElement = document.getElementById('currentDate');
    if (!dateElement) return;
    
    const now = new Date();
    
    switch(period) {
        case 'today':
            dateElement.textContent = now.toLocaleDateString('en-US', { 
                weekday: 'long', 
                month: 'long', 
                day: 'numeric' 
            });
            break;
        case 'month':
            dateElement.textContent = now.toLocaleDateString('en-US', { 
                month: 'long', 
                year: 'numeric' 
            });
            break;
        case 'year':
            dateElement.textContent = now.toLocaleDateString('en-US', { 
                year: 'numeric' 
            });
            break;
        default:
            dateElement.textContent = now.toLocaleDateString('en-US', { 
                month: 'long', 
                year: 'numeric' 
            });
    }
}

// ==================== INITIALIZATION ====================

async function refreshDashboard() {
    console.log('=== REFRESHING DASHBOARD FOR PERIOD:', currentPeriod);
    
    // Update date display
    updateDateDisplay(currentPeriod);
    
    // Show loading states
    showLoadingStates();
    
    try {
        await fetchElectricityData();
        await fetchSavingsData();
        console.log('=== DASHBOARD REFRESHED ===');
    } catch (error) {
        console.error('Error refreshing dashboard:', error);
    } finally {
        // Hide loading states
        hideLoadingStates();
    }
}

function showLoadingStates() {
    // Add loading class to all buttons
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.add('loading');
    });
    
    // Show loading text in key elements
    const loadingElements = ['wastedAmount', 'savedAmount', 'netSavings', 'totalCost', 'usageTillNow', 'usagePredicted'];
    loadingElements.forEach(id => {
        const element = document.getElementById(id);
        if (element) element.textContent = 'Loading...';
    });
}

function hideLoadingStates() {
    // Remove loading class from buttons
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.remove('loading');
    });
}

window.addEventListener('DOMContentLoaded', () => {
    console.log('=== ECOTRACK DASHBOARD INITIALIZED ===');
    
    // Setup time filter buttons
    setupTimeFilters();
    
    // Start the dashboard
    refreshDashboard();
    
    // Set refresh interval
    setInterval(refreshDashboard, REFRESH_INTERVAL);
    
    // Manual trigger for debugging
    window.debugSavings = () => {
        console.log('=== MANUAL SAVINGS UPDATE ===');
        fetchSavingsData();
    };
    
    console.log('Debug function available: window.debugSavings()');
    console.log('=== INITIALIZATION COMPLETE ===');
});