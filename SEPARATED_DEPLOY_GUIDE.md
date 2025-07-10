# 🚀 TGDrive Separated Deployment Guide

## 🎯 **ARSITEKTUR BARU**

TGDrive sekarang terdiri dari **2 service terpisah**:

### 🤖 **Bot Service** (`bot_service.py`)
- ✅ Handles Telegram bot operations
- ✅ Manages file uploads/downloads  
- ✅ Runs independently, tidak restart saat web diubah
- ✅ Menghindari flood wait karena tidak sering restart

### 🌐 **Web Service** (`web_service.py`) 
- ✅ Handles FastAPI web interface
- ✅ Serves website dan API endpoints
- ✅ Bisa restart kapan saja tanpa ganggu bot
- ✅ Komunikasi dengan bot via shared files

---

## 🛠️ **CARA DEPLOY**

### **Opsi 1: Start Semua Service (Recommended)**
```bash
# Start bot + web sekaligus
python3 manage.py start-all

# Check status
python3 manage.py status
```

### **Opsi 2: Start Service Terpisah**
```bash
# Start bot service dulu (harus duluan)
python3 manage.py start-bot

# Start web service (setelah bot running)
python3 manage.py start-web

# Custom port/host
python3 manage.py start-web --host 0.0.0.0 --port 8080
```

---

## 🔧 **MANAGEMENT COMMANDS**

### **Bot Service**
```bash
python3 manage.py start-bot      # Start bot
python3 manage.py stop-bot       # Stop bot  
python3 manage.py restart-bot    # Restart bot
```

### **Web Service**  
```bash
python3 manage.py start-web      # Start web
python3 manage.py stop-web       # Stop web
python3 manage.py restart-web    # Restart web
```

### **All Services**
```bash
python3 manage.py start-all      # Start both
python3 manage.py stop-all       # Stop both
python3 manage.py status         # Check status
```

---

## 🎯 **KEUNTUNGAN SISTEM BARU**

### ✅ **No More Flood Wait**
- Bot tidak restart saat web diubah
- Koneksi Telegram tetap stabil
- Token tidak kena limit berulang

### ✅ **Independent Deploy**
- Edit website → restart web saja
- Edit bot logic → restart bot saja  
- Git pull → pilih service mana yang restart

### ✅ **Better Monitoring**
- Status terpisah untuk bot dan web
- Health check untuk each service
- PID tracking dan process management

### ✅ **Production Ready**
- Process isolation
- Graceful shutdown
- Error recovery per service

---

## 📊 **MONITORING & STATUS**

### **Check Service Status**
```bash
python3 manage.py status
```

Output:
```
📊 TGDrive Service Status
========================================
🤖 Bot Service: 🟢 RUNNING
   PID: 12345
   Status: running
   Clients: 1

🌐 Web Service: 🟢 RUNNING  
   PID: 12346
   Status: running
   Port: 8000

🏥 Overall Health: 🟢 HEALTHY
```

### **Manual Check**
```bash
# Check bot status via API
curl http://localhost:8000/api/bot/status

# Check system health  
curl http://localhost:8000/api/health
```

---

## 🔄 **WORKFLOW DEVELOPMENT**

### **Scenario 1: Edit Website Only**
```bash
# Edit HTML/CSS/JS files
nano templates/index.html

# Restart web service only (bot tetap jalan)
python3 manage.py restart-web
```

### **Scenario 2: Edit Bot Logic**
```bash  
# Edit bot-related code
nano bot_service.py

# Restart bot service only  
python3 manage.py restart-bot
```

### **Scenario 3: Git Pull Update**
```bash
git pull origin main

# Choose what to restart:
python3 manage.py restart-web    # If web changes
python3 manage.py restart-bot    # If bot changes  
python3 manage.py restart-all    # If both changed
```

---

## 🚨 **TROUBLESHOOTING**

### **Bot Service Won't Start**
```bash
# Check bot status
python3 manage.py status

# Check logs
python3 bot_service.py

# Test flood wait
python3 check_flood_wait.py
```

### **Web Service Won't Start**  
```bash
# Check if port is in use
netstat -tlnp | grep :8000

# Start on different port
python3 manage.py start-web --port 8080
```

### **Services Not Communicating**
```bash
# Check shared directory
ls -la shared/

# Test communication
curl http://localhost:8000/api/health
```

---

## 📁 **FILE STRUCTURE**

```
TGDrive/
├── bot_service.py          # Bot service (separate process)
├── web_service.py          # Web service (separate process)  
├── main.py                 # Web entry point (uvicorn)
├── manage.py               # Service manager
├── shared/                 # Communication files
│   ├── bot_status.json
│   ├── web_status.json
│   ├── drive_sync.json
│   └── commands.json
├── pids/                   # Process ID files
│   ├── bot.pid
│   └── web.pid
└── utils/
    ├── shared_comm.py      # Communication system
    ├── clients.py          # Simplified (no Tor)
    └── directoryHandler.py # Fixed error handling
```

---

## ⚡ **QUICK START**

1. **Update bot token (if needed)**:
   ```bash
   python3 update_bot_token.py 7123456789:AAGxxxxx
   ```

2. **Clear old cache**:
   ```bash
   rm -rf cache/
   ```

3. **Start all services**:
   ```bash
   python3 manage.py start-all
   ```

4. **Check status**:
   ```bash
   python3 manage.py status
   ```

5. **Access website**:
   ```
   http://localhost:8000
   ```

---

## 🎉 **MIGRATION SUMMARY**

### **Before (Old System)**
- ❌ Bot + Web in same process
- ❌ Restart everything = flood wait
- ❌ Tor proxy issues
- ❌ Hard to debug

### **After (New System)**  
- ✅ Bot + Web separated
- ✅ Independent restarts
- ✅ No Tor dependency
- ✅ Better monitoring
- ✅ Production ready

**Result: No more flood wait, stable deployment! 🎉**