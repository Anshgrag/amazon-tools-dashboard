# 📋 EcoTrack System Requirements

## 🖥️ **System Requirements**

### 💻 **Minimum Requirements**
- **Operating System**: Windows 10/11, macOS 10.14+, Ubuntu 18.04+ or equivalent
- **Processor**: Intel Core i3 / AMD Ryzen 3 or equivalent
- **Memory (RAM)**: 4GB minimum, 8GB recommended
- **Storage**: 2GB free space
- **Network**: Stable internet connection

### ⚡ **Recommended Requirements**
- **Operating System**: Windows 11, macOS 12+, Ubuntu 20.04+ or latest LTS
- **Processor**: Intel Core i5 / AMD Ryzen 5 or equivalent
- **Memory (RAM)**: 8GB minimum, 16GB recommended
- **Storage**: 5GB free space
- **Network**: Broadband internet connection

## 🔧 **Software Requirements**

### 📦 **Required Software**
```yaml
# Core Runtime
Python 3.8+ (recommended: 3.12.3)

# Web Server
HTTP server for frontend (Python built-in, Node.js, Apache, Nginx)

# Database
SQLite 3.x (comes with Python)

# Web Browser
Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
```

### 📚 **Language & Framework Versions**
```json
{
  "backend": {
    "python": "3.12.3",
    "flask": "3.0.3",
    "flask-cors": "4.0.0",
    "tuya-connector-python": "0.2.0",
    "requests": "2.31.0",
    "sqlite3": "Built-in with Python 3.12.3"
  },
  "frontend": {
    "html5": "Living Standard",
    "css3": "Latest",
    "javascript": "ES6+ (ES2020)",
    "chartjs": "4.4.0"
  }
}
```

## 🔌 **Development Environment Setup**

### 🛠️ **Backend Development Tools**
```bash
# Python Environment
python3 --version  # Should be 3.8+
pip3 --version

# Install dependencies
pip3 install -r requirements.txt

# Development server
cd backend
python3 app.py  # Runs on http://localhost:5000
```

### 🎨 **Frontend Development Tools**
```bash
# Static file server
cd frontend
python3 -m http.server 8000  # Runs on http://localhost:8000

# Alternative: Node.js
npm install -g serve
cd frontend
serve -s 8000
```

### 🐛 **Recommended Development Tools**
```yaml
IDE/Editors:
  - VS Code (recommended)
  - PyCharm Professional
  - WebStorm
  
VS Code Extensions:
  - Python Extension
  - Live Server
  - Prettier
  - Thunder Client (API testing)
  
Browser Developer Tools:
  - Chrome DevTools
  - Firefox Developer Tools
  - Safari Web Inspector
```

## 🌐 **Runtime Dependencies**

### 📦 **Backend Dependencies** (requirements.txt)
```txt
Flask==3.0.3              # Web framework
flask-cors==4.0.0          # Cross-origin resource sharing
tuya-connector-python==0.2.0  # Tuya IoT platform
requests==2.31.0             # HTTP library
sqlite3                       # Database (built-in)
```

### 🌍 **Frontend Dependencies**
```html
<!-- Chart Library -->
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>

<!-- No build tools required - Pure HTML/CSS/JavaScript -->
```

## 🗄️ **Database Requirements**

### 💾 **SQLite Database**
- **Type**: SQLite 3.x
- **File**: `ecotrack.db` (auto-created)
- **Location**: Same directory as `app.py`
- **Backup**: Manual backup of `.db` file recommended

### 📊 **Database Schema**
```sql
-- Core tables
CREATE TABLE electricity_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    device_name TEXT NOT NULL,
    mode TEXT NOT NULL,
    voltage REAL NOT NULL,
    power_watts REAL NOT NULL,
    timestamp TEXT NOT NULL,
    auto_controlled BOOLEAN DEFAULT FALSE,
    manual_override BOOLEAN DEFAULT FALSE,
    device_type TEXT DEFAULT 'unknown',
    rated_power REAL DEFAULT 0
);

CREATE TABLE device_profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    device_name TEXT UNIQUE NOT NULL,
    device_type TEXT NOT NULL,
    rated_power REAL NOT NULL,
    sleep_threshold REAL NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE device_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    device_name TEXT NOT NULL,
    event_type TEXT NOT NULL,
    power_watts REAL NOT NULL,
    duration_minutes INTEGER NOT NULL,
    cost_wasted REAL NOT NULL,
    timestamp TEXT NOT NULL,
    auto_saved BOOLEAN DEFAULT FALSE
);
```

## 🌐 **Network Requirements**

### 📡 **Port Configuration**
```yaml
Backend API:
  Port: 5000
  Protocol: HTTP
  Host: localhost (development)
  CORS: Enabled for http://localhost:8000

Frontend Server:
  Port: 8000
  Protocol: HTTP
  Host: localhost (development)
  Static Files: HTML, CSS, JavaScript, images
```

### 🔗 **External API Requirements**
```yaml
Tuya Cloud API:
  - API Key (from tinytuya.json)
  - API Secret (from tinytuya.json)  
  - API Region (from tinytuya.json)
  - Device ID (from tinytuya.json)
  - Internet Connection: Required
```

## 📱 **Browser Compatibility**

### ✅ **Supported Browsers**
| Browser | Minimum Version | Recommended Version | Notes |
|---------|----------------|-------------------|-------|
| Chrome | 90+ | 120+ | Full support |
| Firefox | 88+ | 115+ | Full support |
| Safari | 14+ | 16+ | Full support |
| Edge | 90+ | 120+ | Full support |
| Opera | 76+ | 100+ | Full support |

### 🚫 **Unsupported Browsers**
- Internet Explorer (any version)
- Edge Legacy (before Chromium)
- Safari < 14
- Chrome < 90
- Firefox < 88

## 🖥️ **Operating System Compatibility**

### ✅ **Supported OS**
| Platform | Minimum | Recommended | Notes |
|----------|----------|-------------|-------|
| Windows | Windows 10 | Windows 11 | Python 3.8+ required |
| macOS | 10.14 Mojave | 12+ Monterey | Use Homebrew for Python |
| Linux | Ubuntu 18.04 | Ubuntu 20.04+ | apt package manager |
| Raspberry Pi | 4+ | Latest | ARM64 support |

### 📦 **Installation by OS**

#### **Windows**
```powershell
# Install Python
winget install Python.Python.3

# Install dependencies
pip install flask flask-cors requests

# Run application
cd backend
python app.py
```

#### **macOS**
```bash
# Install Python (if not installed)
brew install python3

# Install dependencies
pip3 install flask flask-cors requests

# Run application
cd backend
python3 app.py
```

#### **Linux (Ubuntu/Debian)**
```bash
# Update packages
sudo apt update && sudo apt install python3 python3-pip

# Install Python packages
pip3 install flask flask-cors requests

# Run application
cd backend
python3 app.py
```

## 🔧 **Development Workflow**

### 🚀 **Quick Start**
```bash
# 1. Clone/Download project
cd EcoTrack

# 2. Install backend dependencies
cd backend
pip3 install -r requirements.txt

# 3. Start backend server
python3 app.py &

# 4. Start frontend server (new terminal)
cd ../frontend
python3 -m http.server 8000

# 5. Open browser
# Navigate to: http://localhost:8000
```

### 📝 **Development Commands**
```bash
# Backend development
cd backend
python3 app.py                    # Start development server
python3 -m unittest discover      # Run tests
python3 app.py --debug           # Debug mode (if implemented)

# Frontend development  
cd frontend
python3 -m http.server 8000      # Start dev server
python3 -m http.server 8001      # Different port (if needed)

# Database operations
sqlite3 ecotrack.db ".tables"      # List tables
sqlite3 ecotrack.db ".schema"      # Show schema
sqlite3 ecotrack.db "SELECT * FROM electricity_data LIMIT 5;"  # Query data
```

## 🔌 **Hardware Requirements for Smart Plugs**

### 🏠 **IoT Device Requirements**
- **Tuya Compatible Smart Plugs** (16A recommended)
- **WiFi Network**: 2.4GHz or 5GHz
- **Internet Connection**: Stable broadband
- **Mobile Phone**: For Tuya app setup (initial configuration)

### 📡 **Network Setup**
```yaml
WiFi Requirements:
  - Standard: 802.11b/g/n (2.4GHz)
  - Optional: 802.11a/n/ac (5GHz)
  - Security: WPA2/WPA3 recommended
  - Bandwidth: 2Mbps+ per device sufficient

Router Configuration:
  - Ports 5000 & 8000 open for local development
  - DNS: Working internet connection
  - Firewall: Allow Python HTTP traffic
```

## 🐛 **Troubleshooting**

### ❌ **Common Issues**
```yaml
Problem: Backend won't start
Solution: 
  - Check Python version: python3 --version
  - Install missing: pip3 install -r requirements.txt
  - Check port 5000 not in use

Problem: Frontend won't load API
Solution:
  - Verify backend running on localhost:5000
  - Check browser console for CORS errors
  - Confirm both servers on same machine

Problem: Database errors
Solution:
  - Check write permissions in directory
  - Delete ecotrack.db and restart backend
  - Verify SQLite available: sqlite3 --version

Problem: Smart plug control not working
Solution:
  - Verify tinytuya.json configuration
  - Check internet connection
  - Confirm Tuya API credentials valid
```

## 📈 **Performance Considerations**

### ⚡ **Optimization Tips**
```yaml
Database Performance:
  - Limit queries with LIMIT clause
  - Add indexes on timestamp columns
  - Regular cleanup of old data (optional)

Frontend Performance:
  - Enable browser caching
  - Minimize API calls
  - Use debouncing for real-time updates

Memory Usage:
  - Monitor Python memory usage
  - Restart backend if memory leaks detected
  - Use pagination for large datasets
```

## 🔐 **Security Considerations**

### 🛡️ **Security Checklist**
```yaml
Development Environment:
  - Do not expose ports 5000/8000 to internet
  - Use firewall to block external access
  - Keep tinytuya.json secure (don't commit to git)
  
Production Deployment:
  - Use HTTPS certificates
  - Implement authentication
  - Rate limiting for API endpoints
  - Regular security updates
  - Environment variables for secrets
```

---

## ✅ **Summary**

**Minimum Viable Setup:**
- Python 3.8+ + Flask + Modern web browser
- 4GB RAM + 2GB storage + Internet connection

**Recommended Setup:**
- Python 3.12.3 + 16GB RAM + SSD storage + Broadband
- VS Code + Chrome/Edge/Firefox latest
- Tuya-compatible smart plugs + WiFi network

**The system is designed to be lightweight and accessible while providing professional energy management capabilities!** 🌱✨