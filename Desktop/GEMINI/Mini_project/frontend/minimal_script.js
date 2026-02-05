// Minimal working dashboard - let's replace the problematic sections
console.log('=== MINIMAL DASHBOARD LOADING ===');

// Configuration
const API_BASE_URL = 'http://localhost:5000';

// Simple currency formatter
function formatCurrency(value) {
    return `$${parseFloat(value).toFixed(2)}`;
}

// Main update function
async function updateSavingsMonitor() {
    console.log('=== UPDATING SAVINGS MONITOR ===');
    
    try {
        // Test direct API call
        const response = await fetch(`${API_BASE_URL}/api/savings`);
        console.log('API Response Status:', response.status);
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        const result = await response.json();
        console.log('API Response Data:', result);
        
        if (result.status !== 'success') {
            throw new Error('API returned error');
        }
        
        const data = result.data;
        console.log('Processing data:', data);
        
        // Update main display elements
        const elements = {
            wasted: document.getElementById('wastedAmount'),
            saved: document.getElementById('savedAmount'),
            net: document.getElementById('netSavings'),
            percentage: document.getElementById('savingsPercentage')
        };
        
        // Check if elements exist
        console.log('Element check:');
        Object.keys(elements).forEach(key => {
            console.log(`${key}:`, !!elements[key]);
            if (!elements[key]) {
                console.error(`Missing element: ${key}`);
            }
        });
        
        // Update values if elements exist
        if (elements.wasted) {
            const wasteValue = formatCurrency(data.total_waste_cost || 0);
            console.log('Setting waste to:', wasteValue);
            elements.wasted.textContent = wasteValue;
            elements.wasted.style.color = '#ff4757'; // Make it visible
        }
        
        if (elements.saved) {
            const savedValue = formatCurrency(data.total_saved_cost || 0);
            console.log('Setting saved to:', savedValue);
            elements.saved.textContent = savedValue;
            elements.saved.style.color = '#06ffa5'; // Make it visible
        }
        
        if (elements.net) {
            const netValue = formatCurrency(data.net_savings || 0);
            console.log('Setting net to:', netValue);
            elements.net.textContent = netValue;
            elements.net.style.color = '#4ecdc4'; // Make it visible
        }
        
        if (elements.percentage) {
            const total = (data.total_waste_cost || 0) + (data.total_saved_cost || 0);
            const percentage = total > 0 ? ((data.total_saved_cost || 0) / total * 100) : 0;
            const percentageText = `${percentage.toFixed(1)}%`;
            console.log('Setting percentage to:', percentageText);
            elements.percentage.textContent = percentageText;
            elements.percentage.style.color = '#06ffa5'; // Make it visible
        }
        
        console.log('=== SAVINGS MONITOR UPDATED ===');
        
    } catch (error) {
        console.error('ERROR updating savings monitor:', error);
        console.error('Stack:', error.stack);
        
        // Show error on page
        const elements = ['wastedAmount', 'savedAmount', 'netSavings'];
        elements.forEach(id => {
            const el = document.getElementById(id);
            if (el) {
                el.textContent = 'ERROR';
                el.style.color = '#ff4757';
                el.style.fontSize = '1.2em';
            }
        });
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    console.log('=== PAGE LOADED - INITIALIZING ===');
    
    // Wait a moment then update
    setTimeout(() => {
        console.log('Starting savings update...');
        updateSavingsMonitor();
        
        // Update every 30 seconds
        setInterval(updateSavingsMonitor, 30000);
    }, 1000);
});

// Manual update function for debugging
window.updateSavingsMonitor = updateSavingsMonitor;