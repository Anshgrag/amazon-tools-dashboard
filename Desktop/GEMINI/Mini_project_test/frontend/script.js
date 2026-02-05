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
        case 'devices':
            fetchDevicesData();
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

async function fetchDevicesData() {
    try {
        console.log('=== FETCHING DEVICES DATA ===');
        const response = await fetch(`${API_BASE_URL}/api/devices`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        
        if (result.status === 'success') {
            updateDevicesTab(result.data);
        }
    } catch (error) {
        console.error('Error fetching devices data:', error);
        updateDevicesTab(getMockDevices());
    }
}

function getMockDevices() {
    return {
        devices: [
            { id: 1, name: 'TV', type: 'entertainment', status: 'on', power: 120, room: 'living-room', scheduled: false },
            { id: 2, name: 'Router', type: 'network', status: 'on', power: 15, room: 'living-room', scheduled: true },
            { id: 3, name: 'Refrigerator', type: 'kitchen', status: 'on', power: 150, room: 'kitchen', scheduled: false },
            { id: 4, name: 'Charger', type: 'electronics', status: 'off', power: 0, room: 'bedroom', scheduled: false },
            { id: 5, name: 'Office Light', type: 'lighting', status: 'on', power: 45, room: 'office', scheduled: true },
            { id: 6, name: 'AC Unit', type: 'climate', status: 'off', power: 0, room: 'living-room', scheduled: true }
        ],
        schedules: [
            { device: 'TV', start: '22:00', end: '06:00', enabled: true },
            { device: 'Office Light', start: '08:00', end: '18:00', enabled: true },
            { device: 'AC Unit', start: '12:00', end: '14:00', enabled: false }
        ]
    };
}

function updateDevicesTab(data) {
    const devices = data.devices || [];
    const schedules = data.schedules || [];
    
    document.getElementById('totalDevices').textContent = devices.length;
    document.getElementById('activeDevices').textContent = devices.filter(d => d.status === 'on').length;
    document.getElementById('scheduledDevices').textContent = devices.filter(d => d.scheduled).length;
    
    updateDevicesGrid(devices);
    updateSchedulesList(schedules);
    
    setupDeviceControlListeners();
}

function updateDevicesGrid(devices) {
    const grid = document.getElementById('devicesGrid');
    if (!grid) return;
    
    const typeIcons = {
        'entertainment': '📺',
        'network': '📡',
        'kitchen': '🍳',
        'electronics': '🔌',
        'lighting': '💡',
        'climate': '❄️'
    };
    
    const roomNames = {
        'living-room': 'Living Room',
        'kitchen': 'Kitchen',
        'bedroom': 'Bedroom',
        'office': 'Office'
    };
    
    let html = '<div class="devices-cards">';
    devices.forEach(device => {
        const icon = typeIcons[device.type] || '📱';
        const isOn = device.status === 'on';
        const hasSchedule = device.scheduled;
        
        html += `
            <div class="device-card ${isOn ? 'active' : 'inactive'}" data-device-id="${device.id}">
                <div class="device-card-header">
                    <span class="device-icon">${icon}</span>
                    <span class="device-toggle">
                        <input type="checkbox" class="toggle-switch" 
                            id="toggle-${device.id}" 
                            ${isOn ? 'checked' : ''}
                            data-device-id="${device.id}">
                        <label for="toggle-${device.id}" class="toggle-label"></label>
                    </span>
                </div>
                <div class="device-card-name">${device.name}</div>
                <div class="device-card-room">${roomNames[device.room] || device.room}</div>
                <div class="device-card-power">
                    <span class="power-value">${device.power}W</span>
                    <span class="power-status ${isOn ? 'on' : 'off'}">${isOn ? 'ON' : 'OFF'}</span>
                </div>
                ${hasSchedule ? '<span class="device-scheduled">⏰ Scheduled</span>' : ''}
            </div>
        `;
    });
    html += '</div>';
    
    grid.innerHTML = html;
}

function updateSchedulesList(schedules) {
    const list = document.getElementById('schedulesList');
    if (!list) return;
    
    if (!schedules || schedules.length === 0) {
        list.innerHTML = '<div class="no-schedules">No schedules configured</div>';
        return;
    }
    
    let html = '';
    schedules.forEach((schedule, index) => {
        const statusClass = schedule.enabled ? 'enabled' : 'disabled';
        const statusText = schedule.enabled ? 'Active' : 'Disabled';
        
        html += `
            <div class="schedule-item">
                <div class="schedule-info">
                    <span class="schedule-device">${schedule.device}</span>
                    <span class="schedule-time">${schedule.start} - ${schedule.end}</span>
                </div>
                <div class="schedule-status ${statusClass}">${statusText}</div>
                <button class="schedule-delete" data-index="${index}">✕</button>
            </div>
        `;
    });
    
    list.innerHTML = html;
}

function setupDeviceControlListeners() {
    const toggles = document.querySelectorAll('.toggle-switch');
    toggles.forEach(toggle => {
        toggle.addEventListener('change', function() {
            const deviceId = this.getAttribute('data-device-id');
            const isOn = this.checked;
            toggleDevice(deviceId, isOn);
        });
    });
    
    const turnAllOff = document.getElementById('turnAllOff');
    if (turnAllOff) {
        turnAllOff.addEventListener('click', () => turnAllDevices(false));
    }
    
    const turnAllOn = document.getElementById('turnAllOn');
    if (turnAllOn) {
        turnAllOn.addEventListener('click', () => turnAllDevices(true));
    }
    
    const ecoMode = document.getElementById('ecoMode');
    if (ecoMode) {
        ecoMode.addEventListener('click', enableEcoMode);
    }
}

function toggleDevice(deviceId, isOn) {
    console.log(`Turning ${isOn ? 'ON' : 'OFF'} device ${deviceId}`);
    
    const card = document.querySelector(`.device-card[data-device-id="${deviceId}"]`);
    if (card) {
        card.classList.toggle('active', isOn);
        card.classList.toggle('inactive', !isOn);
        
        const powerValue = card.querySelector('.power-value');
        const powerStatus = card.querySelector('.power-status');
        
        if (powerValue) powerValue.textContent = isOn ? '120W' : '0W';
        if (powerStatus) {
            powerStatus.textContent = isOn ? 'ON' : 'OFF';
            powerStatus.className = `power-status ${isOn ? 'on' : 'off'}`;
        }
    }
    
    updateActiveDeviceCount();
}

function turnAllDevices(isOn) {
    console.log(`Turning all devices ${isOn ? 'ON' : 'OFF'}`);
    
    const toggles = document.querySelectorAll('.toggle-switch');
    toggles.forEach(toggle => {
        toggle.checked = isOn;
        
        const deviceId = toggle.getAttribute('data-device-id');
        const card = document.querySelector(`.device-card[data-device-id="${deviceId}"]`);
        if (card) {
            card.classList.toggle('active', isOn);
            card.classList.toggle('inactive', !isOn);
            
            const powerValue = card.querySelector('.power-value');
            const powerStatus = card.querySelector('.power-status');
            
            if (powerValue) powerValue.textContent = isOn ? '120W' : '0W';
            if (powerStatus) {
                powerStatus.textContent = isOn ? 'ON' : 'OFF';
                powerStatus.className = `power-status ${isOn ? 'on' : 'off'}`;
            }
        }
    });
    
    updateActiveDeviceCount();
}

function enableEcoMode() {
    console.log('Enabling Eco Mode');
    
    const toggles = document.querySelectorAll('.toggle-switch');
    toggles.forEach(toggle => {
        const deviceId = toggle.getAttribute('data-device-id');
        const card = document.querySelector(`.device-card[data-device-id="${deviceId}"]`);
        
        if (card && card.querySelector('.device-icon').textContent.includes('🌡️')) {
            toggle.checked = false;
            toggleDevice(deviceId, false);
        }
    });
    
    alert('Eco Mode enabled! Non-essential devices have been turned off.');
}

function updateActiveDeviceCount() {
    const activeCount = document.querySelectorAll('.device-card.active').length;
    document.getElementById('activeDevices').textContent = activeCount;
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
                        maxTicksLimit: 6,
                        maxTicks
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

// ==================== INITIALIZATION ====================

async function refreshDashboard() {
    console.log('=== REFRESHING DASHBOARD FOR PERIOD:', currentPeriod);
    
    updateDateDisplay(currentPeriod);
    
    showLoadingStates();
    
    try {
        await fetchElectricityData();
        await fetchSavingsData();
        console.log('=== DASHBOARD REFRESHED ===');
    } catch (error) {
        console.error('Error refreshing dashboard:', error);
    } finally {
        hideLoadingStates();
    }
}

function showLoadingStates() {
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.add('loading');
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

// ==================== THEME SWITCHING ====================

const themes = {
    dark: {
        name: 'Modern Dark',
        font: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
        'bg-primary': '#1a2332',
        'bg-secondary': '#243447',
        'bg-card': '#2a3f5f',
        'text-primary': '#ffffff',
        'text-secondary': '#b0c4de',
        'accent-teal': '#4ecdc4',
        'accent-yellow': '#ffd166',
        'accent-pink': '#ff6b9d',
        'accent-purple': '#c77dff',
        'accent-green': '#06ffa5',
        'accent-red': '#ff4757',
        'border-color': '#3d5a80',
        'border-radius': '15px',
        'card-shadow': '0 4px 15px rgba(0, 0, 0, 0.3)',
        'bg-pattern': 'none',
        'sidebar-pattern': 'none',
        'card-effect': 'none',
        'header-font': 'normal',
        'card-style': 'modern'
    },
    japan: {
        name: 'Japan',
        font: "'Noto Sans JP', 'Segoe UI', sans-serif",
        'bg-primary': '#fef6e4',
        'bg-secondary': '#f3d2c1',
        'bg-card': '#fff8f0',
        'text-primary': '#2d3436',
        'text-secondary': '#636e72',
        'accent-teal': '#00b894',
        'accent-yellow': '#fdcb6e',
        'accent-pink': '#e84393',
        'accent-purple': '#6c5ce7',
        'accent-green': '#00b894',
        'accent-red': '#d63031',
        'border-color': '#d4a574',
        'border-radius': '4px',
        'card-shadow': '0 2px 10px rgba(212, 165, 116, 0.2)',
        'bg-pattern': 'url("data:image/svg+xml,%3Csvg width=\'60\' height=\'60\' viewBox=\'0 0 60 60\' xmlns=\'http://www.w3.org/2000/svg\'%3E%3Cg fill=\'none\' fill-rule=\'evenodd\'%3E%3Cg fill=\'%23d4a574\' fill-opacity=\'0.08\'%3E%3Cpath d=\'M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z\'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")',
        'sidebar-pattern': 'url("data:image/svg+xml,%3Csvg width=\'40\' height=\'40\' viewBox=\'0 0 40 40\' xmlns=\'http://www.w3.org/2000/svg\'%3E%3Cpath d=\'M20 20.5V18H0v-2h20v-2H0v-2h20v-2H0V8h20V6H0V4h20V2H0V0h22v20h2V0h2v20h2V0h2v20h2V0h2v20h2V0h2v20h2v2H0v-.5zM0 20h20v2H0v-2zm0 4h20v2H0v-2zm0 4h20v2H0v-2zm0 4h20v2H0v-2zm4-12h12v2H4v-2zm0 4h12v2H4v-2zm0 4h12v2H4v-2zm0 4h12v2H4v-2zm4-20h8v2H8V4zm0 4h8v2H8V8zm0 4h8v2H8v-2zm0 4h8v2H8v-2zm0 4h8v2H8v-2z\' fill=\'%23d4a574\' fill-opacity=\'0.1\' fill-rule=\'evenodd\'/%3E%3C/svg%3E")',
        'card-effect': 'japanese',
        'header-font': '300',
        'card-style': 'japanese',
        'logo-effect': 'wave',
        'accent-icon': '🌸'
    },
    germany: {
        name: 'Germany',
        font: "'Roboto', 'Segoe UI', sans-serif",
        'bg-primary': '#2d1f0f',
        'bg-secondary': '#4a3728',
        'bg-card': '#3d2b1f',
        'text-primary': '#f5e6d3',
        'text-secondary': '#d4b896',
        'accent-teal': '#5c8a6f',
        'accent-yellow': '#e67e22',
        'accent-pink': '#c0392b',
        'accent-purple': '#8e44ad',
        'accent-green': '#27ae60',
        'accent-red': '#c0392b',
        'border-color': '#8b6914',
        'border-radius': '8px',
        'card-shadow': '0 4px 20px rgba(0, 0, 0, 0.4)',
        'bg-pattern': 'url("data:image/svg+xml,%3Csvg width=\'100\' height=\'100\' viewBox=\'0 0 100 100\' xmlns=\'http://www.w3.org/2000/svg\'%3E%3Cpath d=\'M50 0L100 50L50 100L0 50z\' fill=\'%238b6914\' fill-opacity=\'0.05\'/%3E%3C/svg%3E")',
        'sidebar-pattern': 'url("data:image/svg+xml,%3Csvg width=\'50\' height=\'50\' viewBox=\'0 0 50 50\' xmlns=\'http://www.w3.org/2000/svg\'%3E%3Cpath d=\'M25 0l25 25L25 50L0 25z\' fill=\'%23e67e22\' fill-opacity=\'0.08\'/%3E%3C/svg%3E")',
        'card-effect': 'autumn',
        'header-font': '500',
        'card-style': 'german',
        'logo-effect': 'shield',
        'accent-icon': '🍂'
    },
    scandinavia: {
        name: 'Scandinavia',
        font: "'Raleway', 'Segoe UI', sans-serif",
        'bg-primary': '#f8f9fa',
        'bg-secondary': '#e9ecef',
        'bg-card': '#ffffff',
        'text-primary': '#212529',
        'text-secondary': '#6c757d',
        'accent-teal': '#4dabf7',
        'accent-yellow': '#ffd43b',
        'accent-pink': '#f783ac',
        'accent-purple': '#9775fa',
        'accent-green': '#51cf66',
        'accent-red': '#ff6b6b',
        'border-color': '#dee2e6',
        'border-radius': '12px',
        'card-shadow': '0 2px 15px rgba(0, 0, 0, 0.05)',
        'bg-pattern': 'url("data:image/svg+xml,%3Csvg width=\'60\' height=\'60\' viewBox=\'0 0 60 60\' xmlns=\'http://www.w3.org/2000/svg\'%3E%3Cpath d=\'M30 0l15 15H15L30 0zm0 30l15 15H15l15-15zm0 30l15 15H15l15-15z\' fill=\'%234dabf7\' fill-opacity=\'0.03\'/%3E%3C/svg%3E")',
        'sidebar-pattern': 'url("data:image/svg+xml,%3Csvg width=\'40\' height=\'40\' viewBox=\'0 0 40 40\' xmlns=\'http://www.w3.org/2000/svg\'%3E%3Cpath d=\'M20 0l10 10H10L20 0zm0 20l10 10H10l10-10zm0 20l10 10H10l10-10z\' fill=\'%234dabf7\' fill-opacity=\'0.05\'/%3E%3C/svg%3E")',
        'card-effect': 'nordic',
        'header-font': '300',
        'card-style': 'minimal',
        'logo-effect': 'clean',
        'accent-icon': '❄️'
    },
    tropical: {
        name: 'Tropical',
        font: "'Poppins', 'Segoe UI', sans-serif",
        'bg-primary': '#0d2618',
        'bg-secondary': '#1a4d33',
        'bg-card': '#0f3322',
        'text-primary': '#e8f5e9',
        'text-secondary': '#a5d6a7',
        'accent-teal': '#4dd0e1',
        'accent-yellow': '#ffd54f',
        'accent-pink': '#ff8a80',
        'accent-purple': '#b39ddb',
        'accent-green': '#69f0ae',
        'accent-red': '#ff5252',
        'border-color': '#2e7d32',
        'border-radius': '20px',
        'card-shadow': '0 8px 25px rgba(105, 240, 174, 0.15)',
        'bg-pattern': 'url("data:image/svg+xml,%3Csvg width=\'80\' height=\'80\' viewBox=\'0 0 80 80\' xmlns=\'http://www.w3.org/2000/svg\'%3E%3Cpath d=\'M40 0C40 0 50 20 60 40C60 40 40 40 40 40C40 40 20 40 20 40C20 40 30 20 40 0zM40 80C40 80 50 60 60 40C60 40 40 40 40 40C40 40 20 40 20 40C20 40 30 60 40 80z\' fill=\'%2369f0ae\' fill-opacity=\'0.05\'/%3E%3C/svg%3E")',
        'sidebar-pattern': 'url("data:image/svg+xml,%3Csvg width=\'60\' height=\'60\' viewBox=\'0 0 60 60\' xmlns=\'http://www.w3.org/2000/svg\'%3E%3Ccircle cx=\'30\' cy=\'30\' r=\'20\' fill=\'%234dd0e1\' fill-opacity=\'0.08\'/%3E%3C/svg%3E")',
        'card-effect': 'tropical',
        'header-font': '400',
        'card-style': 'organic',
        'logo-effect': 'vibrant',
        'accent-icon': '🌴'
    },
    nordic: {
        name: 'Nordic Winter',
        font: "'Montserrat', 'Segoe UI', sans-serif",
        'bg-primary': '#0a1628',
        'bg-secondary': '#132744',
        'bg-card': '#1a2d4a',
        'text-primary': '#e3f2fd',
        'text-secondary': '#90caf9',
        'accent-teal': '#80deea',
        'accent-yellow': '#fff59d',
        'accent-pink': '#f48fb1',
        'accent-purple': '#ce93d8',
        'accent-green': '#a5d6a7',
        'accent-red': '#ef9a9a',
        'border-color': '#1e3a5f',
        'border-radius': '16px',
        'card-shadow': '0 4px 20px rgba(128, 222, 234, 0.1)',
        'bg-pattern': 'url("data:image/svg+xml,%3Csvg width=\'100\' height=\'100\' viewBox=\'0 0 100 100\' xmlns=\'http://www.w3.org/2000/svg\'%3E%3Cpath d=\'M50 0L60 40H100L65 65L80 100L50 75L20 100L35 65L0 40H40L50 0z\' fill=\'%2380deea\' fill-opacity=\'0.05\'/%3E%3C/svg%3E")',
        'sidebar-pattern': 'url("data:image/svg+xml,%3Csvg width=\'70\' height=\'70\' viewBox=\'0 0 70 70\' xmlns=\'http://www.w3.org/2000/svg\'%3E%3Ccircle cx=\'35\' cy=\'35\' r=\'30\' fill=\'none\' stroke=\'%2380deea\' stroke-width=\'1\' stroke-opacity=\'0.1\'/%3E%3Ccircle cx=\'35\' cy=\'35\' r=\'20\' fill=\'none\' stroke=\'%2380deea\' stroke-width=\'1\' stroke-opacity=\'0.08\'/%3E%3Ccircle cx=\'35\' cy=\'35\' r=\'10\' fill=\'%2380deea\' fill-opacity=\'0.05\'/%3E%3C/svg%3E")',
        'card-effect': 'aurora',
        'header-font': '300',
        'card-style': 'frosted',
        'logo-effect': 'glow',
        'accent-icon': '✨'
    }
};

function applyTheme(themeName) {
    const theme = themes[themeName];
    if (!theme) return;
    
    const root = document.documentElement;
    const body = document.body;
    
    Object.entries(theme).forEach(([key, value]) => {
        root.style.setProperty(`--${key}`, value);
        if (key === 'font') {
            document.body.style.fontFamily = value;
        }
    });
    
    body.setAttribute('data-theme', themeName);
    body.setAttribute('data-card-style', theme['card-style']);
    
    localStorage.setItem('ecotrack-theme', themeName);
    
    document.querySelectorAll('.theme-btn').forEach(btn => {
        btn.classList.toggle('active', btn.getAttribute('data-theme') === themeName);
    });
    
    document.querySelector('.logo h1').innerHTML = getLogoHTML(themeName);
    
    console.log(`Theme applied: ${theme.name}`);
}

function getLogoHTML(themeName) {
    const logos = {
        dark: 'ECOTRACK',
        japan: 'エコトラック',
        germany: 'ECOTRACK',
        scandinavia: 'ECOTRACK',
        tropical: '🌴 ECOTRACK 🌴',
        nordic: '◆ ECOTRACK ◆'
    };
    return logos[themeName] || 'ECOTRACK';
}

function setupThemeSwitching() {
    console.log('=== SETUP THEME SWITCHING ===');
    
    const savedTheme = localStorage.getItem('ecotrack-theme') || 'dark';
    applyTheme(savedTheme);
    
    document.querySelectorAll('.theme-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const themeName = this.getAttribute('data-theme');
            applyTheme(themeName);
        });
    });
    
    console.log('Theme switching initialized');
}

window.addEventListener('DOMContentLoaded', () => {
    console.log('=== ECOTRACK DASHBOARD INITIALIZED ===');
    
    setupThemeSwitching();
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

// ==================== PARTICLE ANIMATION SYSTEM ====================

let canvas = null;
let ctx = null;
let particles = [];
let animationId = null;
let currentAnimation = 'none';

const particleConfigs = {
    japan: {
        emoji: ['🌸', '🌺', '🍃', '💮'],
        colors: ['#ffb7c5', '#ffc0cb', '#ff69b4', '#ffc0cb', '#ffe4e1'],
        gravity: 0.5,
        wind: 0.3,
        size: { min: 8, max: 20 },
        speed: { min: 0.5, max: 1.5 },
        rotation: true,
        wobble: true
    },
    germany: {
        emoji: ['🍂', '🪵', '🌰', '🍁'],
        colors: ['#e67e22', '#c0392b', '#d35400', '#a04000', '#8b4513'],
        gravity: 0.6,
        wind: 0.4,
        size: { min: 10, max: 25 },
        speed: { min: 0.8, max: 2 },
        rotation: true,
        wobble: true
    },
    nordic: {
        emoji: ['❄️', '✨', '💎', '🌟'],
        colors: ['#80deea', '#ffffff', '#b2ebf2', '#e0f7fa', '#00bcd4'],
        gravity: 0.3,
        wind: 0.2,
        size: { min: 4, max: 12 },
        speed: { min: 0.3, max: 1 },
        rotation: false,
        wobble: true,
        twinkle: true
    },
    tropical: {
        emoji: ['🌴', '🌿', '🍀', '🌺', '🦋'],
        colors: ['#69f0ae', '#4dd0e1', '#00e676', '#00bcd4', '#1de9b6'],
        gravity: 0.4,
        wind: 0.2,
        size: { min: 10, max: 22 },
        speed: { min: 0.4, max: 1.2 },
        rotation: true,
        wobble: true
    },
    scandinavia: {
        emoji: ['❄️', '🔹', '💠', '◇'],
        colors: ['#4dabf7', '#74c0fc', '#a5d8ff', '#ffffff'],
        gravity: 0.35,
        wind: 0.25,
        size: { min: 5, max: 15 },
        speed: { min: 0.4, max: 1.2 },
        rotation: true,
        wobble: false
    },
    dark: {
        emoji: ['✦', '✧', '◦'],
        colors: ['#4ecdc4', '#c77dff', '#06ffa5', '#ff6b9d'],
        gravity: 0.2,
        wind: 0.1,
        size: { min: 3, max: 8 },
        speed: { min: 0.2, max: 0.8 },
        rotation: false,
        wobble: true
    }
};

class Particle {
    constructor(config, canvasWidth, canvasHeight) {
        this.canvasWidth = canvasWidth;
        this.canvasHeight = canvasHeight;
        
        this.x = Math.random() * canvasWidth;
        this.y = -20;
        
        this.size = config.size.min + Math.random() * (config.size.max - config.size.min);
        this.speedY = config.speed.min + Math.random() * (config.speed.max - config.speed.min);
        this.speedX = (Math.random() - 0.5) * config.wind;
        
        this.color = config.colors[Math.floor(Math.random() * config.colors.length)];
        this.emoji = config.emoji[Math.floor(Math.random() * config.emoji.length)];
        
        this.rotation = config.rotation ? Math.random() * 360 : 0;
        this.rotationSpeed = (Math.random() - 0.5) * 2;
        
        this.wobble = config.wobble ? Math.random() * Math.PI * 2 : 0;
        this.wobbleSpeed = 0.02 + Math.random() * 0.02;
        
        this.opacity = 0.7 + Math.random() * 0.3;
        this.twinkle = config.twinkle || false;
        this.twinklePhase = Math.random() * Math.PI * 2;
    }
    
    update() {
        this.y += this.speedY;
        this.x += this.speedX + Math.sin(this.wobble) * 0.5;
        this.wobble += this.wobbleSpeed;
        
        if (this.rotation) {
            this.rotation += this.rotationSpeed;
        }
        
        if (this.twinkle) {
            this.twinklePhase += 0.1;
        }
        
        if (this.y > this.canvasHeight + 20) {
            this.reset();
        }
        
        if (this.x > this.canvasWidth + 20) {
            this.x = -20;
        }
        
        if (this.x < -20) {
            this.x = this.canvasWidth + 20;
        }
    }
    
    reset() {
        this.y = -20;
        this.x = Math.random() * this.canvasWidth;
    }
    
    draw(ctx) {
        ctx.save();
        ctx.translate(this.x, this.y);
        ctx.rotate(this.rotation * Math.PI / 180);
        
        let alpha = this.opacity;
        if (this.twinkle) {
            alpha *= 0.5 + Math.sin(this.twinklePhase) * 0.5;
        }
        ctx.globalAlpha = alpha;
        
        if (this.emoji) {
            ctx.font = `${this.size}px Arial`;
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillText(this.emoji, 0, 0);
        } else {
            ctx.fillStyle = this.color;
            ctx.beginPath();
            ctx.arc(0, 0, this.size / 2, 0, Math.PI * 2);
            ctx.fill();
        }
        
        ctx.restore();
    }
}

function createCanvas() {
    if (canvas) return;
    
    canvas = document.createElement('canvas');
    canvas.id = 'particle-canvas';
    canvas.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 0;
        overflow: hidden;
    `;
    
    document.body.insertBefore(canvas, document.body.firstChild);
    
    ctx = canvas.getContext('2d');
    resizeCanvas();
    
    window.addEventListener('resize', resizeCanvas);
}

function resizeCanvas() {
    if (canvas) {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }
}

function startParticles(themeName) {
    if (!canvas) createCanvas();
    
    stopParticles();
    
    const config = particleConfigs[themeName];
    if (!config) return;
    
    currentAnimation = themeName;
    const particleCount = themeName === 'nordic' ? 50 : themeName === 'japan' ? 30 : 25;
    
    particles = [];
    for (let i = 0; i < particleCount; i++) {
        const particle = new Particle(config, canvas.width, canvas.height);
        particle.y = Math.random() * canvas.height;
        particles.push(particle);
    }
    
    animate();
}

function stopParticles() {
    if (animationId) {
        cancelAnimationFrame(animationId);
        animationId = null;
    }
    particles = [];
}

function animate() {
    if (!ctx || !canvas) return;
    
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    particles.forEach(particle => {
        particle.update();
        particle.draw(ctx);
    });
    
    animationId = requestAnimationFrame(animate);
}

function updateParticlesForTheme(themeName) {
    if (themeName === 'japan' || themeName === 'germany' || 
        themeName === 'nordic' || themeName === 'tropical' || 
        themeName === 'scandinavia' || themeName === 'dark') {
        startParticles(themeName);
    } else {
        stopParticles();
    }
}

// Override applyTheme to include particles
const originalApplyTheme = applyTheme;
applyTheme = function(themeName) {
    originalApplyTheme(themeName);
    updateParticlesForTheme(themeName);
};

// Initialize particles on load
window.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => {
        const savedTheme = localStorage.getItem('ecotrack-theme') || 'dark';
        updateParticlesForTheme(savedTheme);
    }, 500);
});
