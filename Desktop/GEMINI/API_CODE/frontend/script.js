// ==================== CONFIGURATION ====================

const API_BASE_URL = 'http://localhost:5000';
const REFRESH_INTERVAL = 30000;
let currentPeriod = 'month';
let currentTab = 'dashboard';

let costChart = null;
let usageChart = null;
let savingsChart = null;
let costAnalysisChart = null;
let appliancePowerChart = null;
let roomComparisonChart = null;

// ==================== UTILITY FUNCTIONS ====================

function formatCurrency(value) {
    return `$${parseFloat(value).toFixed(2)}`;
}

function formatDate() {
    const now = new Date();
    const options = { month: 'long', year: 'numeric' };
    return now.toLocaleDateString('en-US', options);
}

// ==================== TAB SWITCHING ====================

function setupTabSwitching() {
    console.log('=== SETUP TAB SWITCHING ===');
    const navItems = document.querySelectorAll('.nav-item');
    console.log('Found nav items:', navItems.length);
    
    navItems.forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            
            const tabName = this.getAttribute('data-tab');
            console.log('=== CLICKED TAB:', tabName, '===');
            if (!tabName) return;
            
            if (tabName === currentTab) {
                console.log('Tab already active:', tabName);
                return;
            }
            
            navItems.forEach(nav => {
                nav.classList.remove('active');
                console.log('Removed active from:', nav.getAttribute('data-tab'));
            });
            this.classList.add('active');
            console.log('Added active to:', tabName);
            
            document.querySelectorAll('.tab-pane').forEach(pane => {
                pane.classList.remove('active');
                console.log('Hidden pane:', pane.id);
            });
            
            const tabPane = document.getElementById(`tab-${tabName}`);
            if (tabPane) {
                tabPane.classList.add('active');
                console.log('Shown pane:', tabPane.id);
            }
            
            currentTab = tabName;
            
            refreshTab(tabName);
        });
    });
    
    console.log('Tab switching setup complete');
}

function refreshTab(tabName) {
    switch(tabName) {
        case 'dashboard':
            refreshDashboard();
            break;
        case 'cost':
            fetchCostData();
            break;
        case 'appliances':
            fetchAppliancesData();
            break;
        case 'rooms':
            fetchRoomsData();
            break;
    }
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
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        console.log('Savings data received:', result);
        
        if (result.status === 'success') {
            updateSavingsDisplay(result.data);
        } else {
            console.error('API returned error:', result);
        }
    } catch (error) {
        console.error('Error fetching savings data:', error);
    }
}

async function fetchCostData() {
    try {
        console.log('=== FETCHING COST DATA FOR PERIOD:', currentPeriod);
        const response = await fetch(`${API_BASE_URL}/api/savings?period=${currentPeriod}`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        
        if (result.status === 'success') {
            updateCostAnalysis(result.data);
        }
    } catch (error) {
        console.error('Error fetching cost data:', error);
    }
}

async function fetchAppliancesData() {
    try {
        console.log('=== FETCHING APPLIANCES DATA FOR PERIOD:', currentPeriod);
        const response = await fetch(`${API_BASE_URL}/api/electricity/history?period=${currentPeriod}`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        
        if (result.status === 'success') {
            updateAppliancesTab(result.data);
        }
    } catch (error) {
        console.error('Error fetching appliances data:', error);
    }
}

async function fetchRoomsData() {
    try {
        console.log('=== FETCHING ROOMS DATA FOR PERIOD:', currentPeriod);
        const response = await fetch(`${API_BASE_URL}/api/rooms/usage?period=${currentPeriod}`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        
        if (result.status === 'success') {
            updateRoomsTab(result.data);
        }
    } catch (error) {
        console.error('Error fetching rooms data:', error);
    }
}

// ==================== UPDATE DISPLAY FUNCTIONS ====================

function updateAppliancesDisplay(data) {
    const appliancesList = document.getElementById('appliancesList');
    if (!appliancesList) return;
    
    const deviceMap = {};
    data.forEach(record => {
        if (!deviceMap[record.device_name] || 
            new Date(record.timestamp) > new Date(deviceMap[record.device_name].timestamp)) {
            deviceMap[record.device_name] = record;
        }
    });
    
    const colors = {
        'TV': '#ff6b9d',
        'Router': '#c77dff',
        'Charger': '#4ecdc4',
        'Refrigerator': '#ffd166'
    };
    
    const devices = Object.values(deviceMap).sort((a, b) => b.power_watts - a.power_watts);
    
    let html = '';
    devices.forEach(device => {
        const maxPower = 200;
        const barWidth = Math.min((device.power_watts / maxPower) * 100, 100);
        const color = colors[device.device_name] || '#4ecdc4';
        
        // Update device control status based on mode
        if (device.device_name === 'Smart Switch') {
            const toggle = document.getElementById('deviceToggle');
            const status = document.getElementById('deviceStatus');
            if (device.mode === 'ON' || device.mode === 'Standby') {
                toggle.checked = true;
                status.textContent = 'ON';
                status.className = 'device-status online';
            } else {
                toggle.checked = false;
                status.textContent = 'OFF';
                status.className = 'device-status offline';
            }
        }
        
        html += `
            <div class="appliance-item">
                <div class="appliance-name">${device.device_name}</div>
                <div class="appliance-bar">
                    <div class="appliance-bar-fill" style="width: ${barWidth}%; background: ${color};"></div>
                </div>
                <div class="appliance-value">${device.power_watts.toFixed(1)} W</div>
            </div>
        `;
    });
    
    appliancesList.innerHTML = html;
}

function updateCostPredicted(data) {
    let totalPower = 0;
    data.forEach(record => {
        totalPower += record.power_watts;
    });
    
    const avgPowerKW = totalPower / data.length / 1000;
    const hoursPerMonth = 730;
    const costPerKWh = 0.12;
    const totalCost = avgPowerKW * hoursPerMonth * costPerKWh;
    
    const electricityCost = totalCost * 0.8;
    const gasCost = totalCost * 0.2;
    
    const totalCostElement = document.getElementById('totalCost');
    if (totalCostElement) totalCostElement.textContent = formatCurrency(totalCost);
    
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

// ==================== SAVINGS UPDATE FUNCTIONS ====================

function updateSavingsDisplay(data) {
    console.log('=== UPDATING SAVINGS DISPLAY ===');
    console.log('Data received:', data);
    
    try {
        const wastedAmount = document.getElementById('wastedAmount');
        const savedAmount = document.getElementById('savedAmount');
        const netSavings = document.getElementById('netSavings');
        const savingsPercentage = document.getElementById('savingsPercentage');
        
        if (!wastedAmount || !savedAmount || !netSavings || !savingsPercentage) {
            console.error('Savings display elements not found');
            return;
        }
        
        const totalWaste = parseFloat(data.total_waste_cost) || 0;
        const totalSaved = parseFloat(data.total_saved_cost) || 0;
        const netSavingsValue = parseFloat(data.net_savings) || 0;
        
        const wasteFormatted = formatCurrency(totalWaste);
        const savedFormatted = formatCurrency(totalSaved);
        const netFormatted = formatCurrency(netSavingsValue);
        
        wastedAmount.textContent = wasteFormatted;
        savedAmount.textContent = savedFormatted;
        netSavings.textContent = netFormatted;
        
        const totalPotential = totalWaste + totalSaved;
        const percentage = totalPotential > 0 ? (totalSaved / totalPotential * 100) : 0;
        savingsPercentage.textContent = `${percentage.toFixed(1)}%`;
        
        if (data.device_details && Array.isArray(data.device_details)) {
            updateDeviceSavingsList(data.device_details);
        }
        
        createSavingsChart(totalWaste, totalSaved);
        
    } catch (error) {
        console.error('Error updating savings display:', error);
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

// ==================== COST TAB FUNCTIONS ====================

function updateCostAnalysis(data) {
    const totalWaste = parseFloat(data.total_waste_cost) || 0;
    const totalSaved = parseFloat(data.total_saved_cost) || 0;
    const projectedCost = totalWaste;
    
    document.getElementById('costThisMonth').textContent = formatCurrency(totalWaste);
    document.getElementById('costLastMonth').textContent = formatCurrency(totalWaste * 0.95);
    document.getElementById('costProjected').textContent = formatCurrency(projectedCost);
    
    if (data.device_details && Array.isArray(data.device_details)) {
        updateDeviceCostList(data.device_details);
    }
    
    createCostAnalysisChart(data.device_details || []);
}

function updateDeviceCostList(devices) {
    const deviceCostList = document.getElementById('deviceCostList');
    if (!deviceCostList) return;
    
    if (!devices || devices.length === 0) {
        deviceCostList.innerHTML = '<div class="no-devices">No device data available</div>';
        return;
    }
    
    let html = '';
    devices.forEach(device => {
        const totalCost = (device.waste_cost || 0) + (device.saved_cost || 0);
        html += `
            <div class="device-cost-item">
                <div class="device-name">${device.device_name}</div>
                <div class="device-cost-value">${formatCurrency(totalCost)}</div>
            </div>
        `;
    });
    
    deviceCostList.innerHTML = html;
}

// ==================== APPLIANCES TAB FUNCTIONS ====================

function updateAppliancesTab(data) {
    const deviceMap = {};
    data.forEach(record => {
        if (!deviceMap[record.device_name] || 
            new Date(record.timestamp) > new Date(deviceMap[record.device_name].timestamp)) {
            deviceMap[record.device_name] = record;
        }
    });
    
    const devices = Object.values(deviceMap);
    
    updateAllAppliancesGrid(devices);
    updateApplianceStatusList(devices);
    createAppliancePowerChart(devices);
}

function updateAllAppliancesGrid(devices) {
    const grid = document.getElementById('allAppliancesGrid');
    if (!grid) return;
    
    const colors = {
        'TV': '#ff6b9d',
        'Router': '#c77dff',
        'Charger': '#4ecdc4',
        'Refrigerator': '#ffd166'
    };
    
    let html = '<div class="appliances-cards">';
    devices.forEach(device => {
        const color = colors[device.device_name] || '#4ecdc4';
        const isActive = device.power_watts > 5;
        
        html += `
            <div class="appliance-card" style="border-left: 4px solid ${color};">
                <div class="appliance-card-header">
                    <span class="appliance-card-name">${device.device_name}</span>
                    <span class="appliance-card-status ${isActive ? 'active' : 'inactive'}">
                        ${isActive ? 'ON' : 'OFF'}
                    </span>
                </div>
                <div class="appliance-card-power">${device.power_watts.toFixed(1)} W</div>
                <div class="appliance-card-mode">${device.mode || 'Unknown'}</div>
            </div>
        `;
    });
    html += '</div>';
    
    grid.innerHTML = html;
}

function updateApplianceStatusList(devices) {
    const list = document.getElementById('applianceStatusList');
    if (!list) return;
    
    let html = '';
    devices.forEach(device => {
        const isActive = device.power_watts > 5;
        html += `
            <div class="status-item">
                <span class="status-indicator ${isActive ? 'on' : 'off'}"></span>
                <span class="status-name">${device.device_name}</span>
                <span class="status-power">${device.power_watts.toFixed(1)} W</span>
            </div>
        `;
    });
    
    list.innerHTML = html;
}

// ==================== ROOMS TAB FUNCTIONS ====================

function updateRoomsTab(data) {
    const rooms = data.rooms || {};
    
    document.getElementById('roomLivingRoom').textContent = `${(rooms['living-room'] || 0).toFixed(1)} kWh`;
    document.getElementById('roomKitchen').textContent = `${(rooms['kitchen'] || 0).toFixed(1)} kWh`;
    document.getElementById('roomBedroom').textContent = `${(rooms['bedroom'] || 0).toFixed(1)} kWh`;
    document.getElementById('roomOffice').textContent = `${(rooms['office'] || 0).toFixed(1)} kWh`;
    
    createRoomComparisonChart(rooms);
    updateRoomDetailsList(data.details || []);
}

function updateRoomDetailsList(roomUsage) {
    const list = document.getElementById('roomDetailsList');
    if (!list) return;
    
    const roomNames = {
        'living-room': 'Living Room',
        'kitchen': 'Kitchen',
        'bedroom': 'Bedroom',
        'office': 'Office'
    };
    
    let html = '';
    for (const [room, usage] of Object.entries(roomUsage)) {
        html += `
            <div class="room-detail-item">
                <span class="room-detail-name">${roomNames[room]}</span>
                <span class="room-detail-usage">${usage.toFixed(1)} kWh</span>
            </div>
        `;
    }
    
    list.innerHTML = html;
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
    const ctx = document.getElementById('savingsChart');
    if (!ctx) return;
    
    if (savingsChart) {
        savingsChart.destroy();
    }
    
    const waste = Math.max(0, wasteCost || 0);
    const saved = Math.max(0, savedCost || 0);
    
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
}

function createCostAnalysisChart(devices) {
    const ctx = document.getElementById('costAnalysisChart');
    if (!ctx) return;
    
    if (costAnalysisChart) {
        costAnalysisChart.destroy();
    }
    
    const labels = devices.map(d => d.device_name);
    const wasteData = devices.map(d => d.waste_cost || 0);
    const savedData = devices.map(d => d.saved_cost || 0);
    
    costAnalysisChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Wasted',
                    data: wasteData,
                    backgroundColor: '#ff6b9d',
                    borderRadius: 4
                },
                {
                    label: 'Saved',
                    data: savedData,
                    backgroundColor: '#06ffa5',
                    borderRadius: 4
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                    labels: {
                        color: '#b0c4de'
                    }
                }
            },
            scales: {
                x: {
                    grid: {
                        color: 'rgba(255, 255, 255, 0.05)'
                    },
                    ticks: {
                        color: '#b0c4de'
                    }
                },
                y: {
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
}

function createAppliancePowerChart(devices) {
    const ctx = document.getElementById('appliancePowerChart');
    if (!ctx) return;
    
    if (appliancePowerChart) {
        appliancePowerChart.destroy();
    }
    
    const labels = devices.map(d => d.device_name);
    const powerData = devices.map(d => d.power_watts || 0);
    
    const colors = {
        'TV': '#ff6b9d',
        'Router': '#c77dff',
        'Charger': '#4ecdc4',
        'Refrigerator': '#ffd166'
    };
    
    const backgroundColors = labels.map(l => colors[l] || '#4ecdc4');
    
    appliancePowerChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: powerData,
                backgroundColor: backgroundColors,
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'right',
                    labels: {
                        color: '#b0c4de'
                    }
                }
            }
        }
    });
}

function createRoomComparisonChart(roomUsage) {
    const ctx = document.getElementById('roomComparisonChart');
    if (!ctx) return;
    
    if (roomComparisonChart) {
        roomComparisonChart.destroy();
    }
    
    const labels = ['Living Room', 'Kitchen', 'Bedroom', 'Office'];
    const data = [
        roomUsage['living-room'],
        roomUsage['kitchen'],
        roomUsage['bedroom'],
        roomUsage['office']
    ];
    
    roomComparisonChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Energy Usage (kWh)',
                data: data,
                backgroundColor: ['#4ecdc4', '#ff6b9d', '#ffd166', '#c77dff'],
                borderRadius: 8
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
                    grid: {
                        display: false
                    },
                    ticks: {
                        color: '#b0c4de'
                    }
                },
                y: {
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

// ==================== TIME FILTER FUNCTIONS ====================

function setupTimeFilters() {
    const filterButtons = document.querySelectorAll('.filter-btn');
    
    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            const selectedPeriod = this.textContent.toLowerCase();
            
            if (selectedPeriod === currentPeriod) {
                return;
            }
            
            filterButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            
            currentPeriod = selectedPeriod;
            
            updateDateDisplay(selectedPeriod);
            
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

// ==================== DEVICE CONTROL ====================

async function toggleDevice(deviceId) {
    try {
        const toggle = document.getElementById('deviceToggle');
        const state = toggle.checked ? 'on' : 'off';
        
        console.log(`Toggling device ${deviceId} to ${state}`);
        
        const response = await fetch(`${API_BASE_URL}/api/devices/${deviceId}/toggle`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ state: state })
        });
        
        const result = await response.json();
        
        if (result.status === 'success') {
            console.log(`Device ${deviceId} turned ${state}`);
            updateDeviceStatus(state);
        } else {
            console.error('Failed to toggle device:', result);
            // Revert toggle state on failure
            toggle.checked = !toggle.checked;
        }
    } catch (error) {
        console.error('Error toggling device:', error);
        // Revert toggle state on error
        const toggle = document.getElementById('deviceToggle');
        toggle.checked = !toggle.checked;
    }
}

function updateDeviceStatus(state) {
    const status = document.getElementById('deviceStatus');
    if (state === 'on') {
        status.textContent = 'ON';
        status.className = 'device-status online';
    } else {
        status.textContent = 'OFF';
        status.className = 'device-status offline';
    }
}

// ==================== INITIALIZATION ====================

document.addEventListener('DOMContentLoaded', function() {
    console.log('=== DOMContentLoaded ===');
    setupTabSwitching();
    setupTimeFilters();
    setupThemeToggle();
    initializeCharts();
    fetchAllData();
    
    // Set up periodic data refresh
    setInterval(fetchAllData, REFRESH_INTERVAL);
    
    // Initialize device control
    updateDeviceStatus('on'); // Default to on
});
    
    const loadingElements = ['wastedAmount', 'savedAmount', 'netSavings', 'totalCost', 'usageTillNow', 'usagePredicted'];
    loadingElements.forEach(id => {
        const element = document.getElementById(id);
        if (element) element.textContent = 'Loading...';
    });
}

function hideLoadingStates() {
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.remove('loading');
    });
}

// ==================== LIGHT/DARK THEME TOGGLE ====================

function setupThemeToggle() {
    const themeToggle = document.getElementById('themeToggle');
    if (!themeToggle) return;
    
    const isDark = localStorage.getItem('theme') !== 'light';
    updateTheme(isDark);
    
    themeToggle.addEventListener('click', function() {
        const isCurrentlyDark = document.body.getAttribute('data-theme') === 'dark';
        const newIsDark = !isCurrentlyDark;
        updateTheme(newIsDark);
        localStorage.setItem('theme', newIsDark ? 'dark' : 'light');
    });
}

function updateTheme(isDark) {
    const root = document.documentElement;
    const body = document.body;
    const themeIcon = document.querySelector('.theme-icon');
    
    if (isDark) {
        root.style.setProperty('--bg-primary', '#1a2332');
        root.style.setProperty('--bg-secondary', '#243447');
        root.style.setProperty('--bg-card', '#2a3f5f');
        root.style.setProperty('--text-primary', '#ffffff');
        root.style.setProperty('--text-secondary', '#b0c4de');
        root.style.setProperty('--accent-teal', '#4ecdc4');
        root.style.setProperty('--accent-yellow', '#ffd166');
        root.style.setProperty('--accent-pink', '#ff6b9d');
        root.style.setProperty('--accent-purple', '#c77dff');
        root.style.setProperty('--accent-green', '#06ffa5');
        root.style.setProperty('--accent-red', '#ff4757');
        root.style.setProperty('--border-color', '#3d5a80');
        body.setAttribute('data-theme', 'dark');
        if (themeIcon) themeIcon.textContent = '🌙';
    } else {
        root.style.setProperty('--bg-primary', '#f5f7fa');
        root.style.setProperty('--bg-secondary', '#e8ecf1');
        root.style.setProperty('--bg-card', '#ffffff');
        root.style.setProperty('--text-primary', '#1a2332');
        root.style.setProperty('--text-secondary', '#5a6a7a');
        root.style.setProperty('--accent-teal', '#20b2aa');
        root.style.setProperty('--accent-yellow', '#f0c040');
        root.style.setProperty('--accent-pink', '#e85a7d');
        root.style.setProperty('--accent-purple', '#9b59b6');
        root.style.setProperty('--accent-green', '#2ecc71');
        root.style.setProperty('--accent-red', '#e74c3c');
        root.style.setProperty('--border-color', '#d0d7de');
        body.setAttribute('data-theme', 'light');
        if (themeIcon) themeIcon.textContent = '☀️';
    }
}

window.addEventListener('DOMContentLoaded', () => {
    console.log('=== ECOTRACK DASHBOARD INITIALIZED ===');
    
    setupThemeToggle();
    setupTabSwitching();
    setupTimeFilters();
    
    refreshDashboard();
    
    setInterval(refreshDashboard, REFRESH_INTERVAL);
    
    window.debugSavings = () => {
        console.log('=== MANUAL SAVINGS UPDATE ===');
        fetchSavingsData();
    };
    
    console.log('Debug function available: window.debugSavings()');
    console.log('=== INITIALIZATION COMPLETE ===');
});
