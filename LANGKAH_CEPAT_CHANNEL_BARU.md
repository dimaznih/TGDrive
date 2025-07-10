# 🚀 Langkah Cepat: Buat Channel Storage Baru

## Step 1: Buat Channel (2 menit)
1. **Buka Telegram** → Buat **Channel** baru (bukan group)
2. **Nama:** "TGDrive Storage 2024" atau apapun
3. **Tipe:** Private (untuk keamanan)
4. **Save channel**

## Step 2: Tambahkan Bot (1 menit)  
1. **Di channel baru** → klik nama channel → **Administrators**
2. **Add Administrator** → cari **@Kudobot2bot**
3. **Berikan semua permission** dan save

## Step 3: Dapatkan Channel ID (1 menit)
1. **Kirim message apapun** di channel
2. **Forward message itu** ke @userinfobot  
3. **Copy channel ID** (seperti `-1001234567890`)

## Step 4: Kirim Message Backup Pertama (30 detik)
1. **Di channel baru**, kirim:
   ```
   🔐 TGDrive Database Backup File
   
   Ini adalah backup file untuk TGDrive.
   JANGAN HAPUS MESSAGE INI!
   ```
2. **Ini akan jadi message ID 1**

## Step 5: Update Environment (1 menit)
Edit file `.env`:
```env
API_ID=24783879
API_HASH=935a8934034dfd64ecce5e9854fa071b
BOT_TOKENS=7934604269:AAHNUA-tKN0zjJ0wY1ZOfvQCeFNakY97BNE
STORAGE_CHANNEL=-1001234567890  # ← ID channel baru dari step 3
DATABASE_BACKUP_MSG_ID=1         # ← Message pertama (step 4)
DATABASE_BACKUP_TIME=60
WEBSITE_URL=http://209.74.81.235:8000
MAIN_BOT_TOKEN=7934604269:AAHNUA-tKN0zjJ0wY1ZOfvQCeFNakY97BNE
ADMIN_PASSWORD=123
TELEGRAM_ADMIN_IDS=7691463286,5381870056,5092392994,1841535556,1446366033,6137698413,5366835263
```

## Step 6: Restart (30 detik)
```bash
rm -rf cache/
sudo kill -9 $(sudo lsof -t -i:8000) 2>/dev/null
uvicorn main:app --host 0.0.0.0 --port 8000
```

## ✅ Hasil Yang Diharapkan:
```
✅ utils.clients - INFO - Started - Bot Client 1  
✅ utils.directoryHandler - INFO - Drive data loaded from Telegram backup.
✅ INFO: Uvicorn running on http://0.0.0.0:8000
```

**Total waktu: 5 menit** 🎯