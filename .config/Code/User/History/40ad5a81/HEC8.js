// ==================== CONFIGURATION ====================

// Backend API base URL - change this if backend runs on different server
const API_BASE_URL = 'http://localhost:5000';

// Refresh interval in milliseconds (30 seconds)
const REFRESH_INTERVAL = 30000;

// Chart.js chart objects (global scope)
let aqiChart = null;
let electricityChart = null;

// ==================== AQI HELPER FUNCTIONS ====================

/**
 * Get AQI category and color based on AQI value
 * Based on EPA Air Quality Index standards
 */
function getAQICategory(aqiValue) {
    if (aqiValue <= 50) {
        return { category: 'Good', class: 'aqi-good' };
    } else if (aqiValue <= 100) {
        return { category: 'Moderate', class: 'aqi-moderate' };
    } else if (aqiValue <= 150) {
        return { category: 'Unhealthy for Sensitive Groups', class: 'aqi-unhealthy-sensitive' };
    } else if (aqiValue <= 200) {
        return { category: 'Unhealthy', class: 'aqi-unhealthy' };
    } else if (aqiValue <= 300) {
        return { category: 'Very Unhealthy', class: 'aqi-very-unhealthy' };
    } else {
        return { category: 'Hazardous', class: 'aqi-hazardous' };
    }
}

// ==================== FETCH DATA FUNCTIONS ====================

/**
 * Fetch latest AQI data from backend
 */
async function fetchLatestAQI() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/aqi/latest`);
        const result = await response.json();
        
        if (result.status === 'success') {
            updateAQIDisplay(result.data);
        }
    } catch (error) {
        console.error('Error fetching AQI data:', error);
        document.getElementById('indoorAQI').textContent = 'Error';
        document.getElementById('outdoorAQI').textContent = 'Error';
    }
}

/**
 * Fetch AQI history for chart
 */
async function fetchAQIHistory() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/aqi/history?limit=20`);
        const result = await response.json();
        
        if (result.status === 'success') {
            updateAQIChart(result.data);
        }
    } catch (error) {
        console.error('Error fetching AQI history:', error);
    }
}

/**
 * Fetch electricity data from backend
 */
async function fetchElectricityData() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/electricity/history?limit=50`);
        const result = await response.json();
        
        if (result.status === 'success') {
            updateElectricityDisplay(result.data);
            updateElectricityChart(result.data);
        }
    } catch (error) {
        console.error('Error fetching electricity data:', error);
        document.getElementById('deviceGrid').innerHTML = '<div class="loading">Error loading device data</div>';
    }
}

/**
 * Fetch system statistics
 */
async function fetchSystemStats() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/stats`);
        const result = await response.json();
        
        if (result.status === 'success') {
            document.getElementById('totalDevices').textContent = result.data.device_count;
            document.getElementById('totalRecords').textContent = 
                result.data.total_aqi_records + result.data.total_electricity_records;
        }
    } catch (error) {
        console.error('Error fetching stats:', error);
    }
}

// ==================== UPDATE DISPLAY FUNCTIONS ====================

/**
 * Update AQI display with latest data
 */
function updateAQIDisplay(data) {
    // Update Indoor AQI
    if (data.indoor) {
        const indoorAQI = data.indoor.aqi_value;
        const indoorInfo = getAQICategory(indoorAQI);
        
        document.getElementById('indoorAQI').textContent = indoorAQI;
        const indoorCategoryEl = document.getElementById('indoorCategory');
        indoorCategoryEl.textContent = indoorInfo.category;
        indoorCategoryEl.className = `aqi-category ${indoorInfo.class}`;
    } else {
        document.getElementById('indoorAQI').textContent = 'N/A';
        document.getElementById('indoorCategory').textContent = 'No Data';
    }
    
    // Update Outdoor AQI
    if (data.outdoor) {
        const outdoorAQI = data.outdoor.aqi_value;
        const outdoorInfo = getAQICategory(outdoorAQI);
        
        document.getElementById('outdoorAQI').textContent = outdoorAQI;
        const outdoorCategoryEl = document.getElementById('outdoorCategory');
        outdoorCategoryEl.textContent = outdoorInfo.category;
        outdoorCategoryEl.className = `aqi-category ${outdoorInfo.class}`;
    } else {
        document.getElementById('outdoorAQI').textContent = 'N/A';
        document.getElementById('outdoorCategory').textContent = 'No Data';
    }
}

/**
 * Update electricity device display
 */
function updateElectricityDisplay(data) {
    const deviceGrid = document.getElementById('deviceGrid');
    
    if (data.length === 0) {
        deviceGrid.innerHTML = '<div class="loading">No device data available</div>';
        return;
    }
    
    // Get latest reading for each device
    const deviceMap = {};
    data.forEach(record => {
        if (!deviceMap[record.device_name] || 
            new Date(record.timestamp) > new Date(deviceMap[record.device_name].timestamp)) {
            deviceMap[record.device_name] = record;
        }
    });
    
    // Create HTML for each device
    let html = '';
    Object.values(deviceMap).forEach(device => {
        const modeClass = `mode-${device.mode.toLowerCase()}`;
        html += `
            <div class="device-card">
                <div class="device-name">${device.device_name}</div>
                <div class="device-info">
                    <div class="device-info-item">
                        <span class="device-info-label">Status:</span>
                        <span class="device-info-value ${modeClass}">${device.mode}</span>
                    </div>
                    <div class="device-info-item">
                        <span class="device-info-label">Power:</span>
                        <span class="device-info-value">${device.power_watts.toFixed(2)} W</span>
                    </div>
                    <div class="device-info-item">
                        <span class="device-info-label">Voltage:</span>
                        <span class="device-info-value">${device.voltage.toFixed(2)} V</span>
                    </div>
                    <div class="device-info-item">
                        <span class="device-info-label">Updated:</span>
                        <span class="device-info-value">${formatTime(device.timestamp)}</span>
                    </div>
                </div>
            </div>
        `;
    });
    
    deviceGrid.innerHTML = html;
}

// ==================== CHART FUNCTIONS ====================

/**
 * Create or update AQI line chart
 */
function updateAQIChart(data) {
    // Separate indoor and outdoor data
    const indoorData = data.filter(d => d.location_type === 'indoor').reverse();
    const outdoorData = data.filter(d => d.location_type === 'outdoor').reverse();
    
    // Prepare labels (timestamps)
    const labels = [...new Set([...indoorData, ...outdoorData].map(d => formatTime(d.timestamp)))];
    
    const chartData = {
        labels: labels,
        datasets: [
            {
                label: 'Indoor AQI',
                data: indoorData.map(d => d.aqi_value),
                borderColor: '#3498db',
                backgroundColor: 'rgba(52, 152, 219, 0.1)',
                tension: 0.4,
                fill: true
            },
            {
                label: 'Outdoor AQI',
                data: outdoorData.map(d => d.aqi_value),
                borderColor: '#2ecc71',
                backgroundColor: 'rgba(46, 204, 113, 0.1)',
                tension: 0.4,
                fill: true
            }
        ]
    };
    
    const config = {
        type: 'line',
        data: chartData,
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                },
                title: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'AQI Value'
                    }
                }
            }
        }
    };
    
    // Destroy old chart if exists
    if (aqiChart) {
        aqiChart.destroy();
    }
    
    // Create new chart
    const ctx = document.getElementById('aqiChart').getContext('2d');
    aqiChart = new Chart(ctx, config);
}

/**
 * Create or update electricity bar chart
 */
function updateElectricityChart(data) {
    // Calculate average power per device
    const devicePower = {};
    data.forEach(record => {
        if (!devicePower[record.device_name]) {
            devicePower[record.device_name] = [];
        }
        devicePower[record.device_name].push(record.power_watts);
    });
    
    // Calculate averages
    const devices = Object.keys(devicePower);
    const averages = devices.map(device => {
        const values = devicePower[device];
        return values.reduce((a, b) => a + b, 0) / values.length;
    });
    
    const chartData = {
        labels: devices,
        datasets: [{
            label: 'Average Power Consumption (Watts)',
            data: averages,
            backgroundColor: [
                'rgba(52, 152, 219, 0.7)',
                'rgba(46, 204, 113, 0.7)',
                'rgba(241, 196, 15, 0.7)',
                'rgba(231, 76, 60, 0.7)',
                'rgba(155, 89, 182, 0.7)'
            ],
            borderColor: [
                'rgba(52, 152, 219, 1)',
                'rgba(46, 204, 113, 1)',
                'rgba(241, 196, 15, 1)',
                'rgba(231, 76, 60, 1)',
                'rgba(155, 89, 182, 1)'
            ],
            borderWidth: 2
        }]
    };
    
    const config = {
        type: 'bar',
        data: chartData,
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Power (Watts)'
                    }
                }
            }
        }
    };
    
    // Destroy old chart if exists
    if (electricityChart) {
        electricityChart.destroy();
    }
    
    // Create new chart
    const ctx = document.getElementById('electricityChart').getContext('2d');
    electricityChart = new Chart(ctx, config);
}

// ==================== UTILITY FUNCTIONS ====================

/**
 * Format timestamp to readable time
 */
function formatTime(timestamp) {
    const date = new Date(timestamp);
    return date.toLocaleTimeString('en-US', { 
        hour: '2-digit', 
        minute: '2-digit'
    });
}

/**
 * Update "Last Updated" timestamp
 */
function updateLastUpdatedTime() {
    const now = new Date();
    document.getElementById('lastUpdated').textContent = now.toLocaleString();
}

// ==================== MAIN DATA REFRESH FUNCTION ====================

/**
 * Fetch all data and update dashboard
 */
async function refreshDashboard() {
    console.log('Refreshing dashboard data...');
    
    // Update last updated time
    updateLastUpdatedTime();
    
    // Fetch all data in parallel
    await Promise.all([
        fetchLatestAQI(),
        fetchAQIHistory(),
        fetchElectricityData(),
        fetchSystemStats()
    ]);
}

// ==================== INITIALIZATION ====================

/**
 * Initialize dashboard when page loads
 */
window.addEventListener('DOMContentLoaded', () => {
    console.log('EcoTrack Dashboard Initialized');
    
    // Initial data load
    refreshDashboard();
    
    // Set up automatic refresh every 30 seconds
    setInterval(refreshDashboard, REFRESH_INTERVAL);
    
    console.log(`Auto-refresh enabled: Every ${REFRESH_INTERVAL / 1000} seconds`);
});
