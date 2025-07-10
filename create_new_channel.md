# Buat Channel Storage Baru

## Langkah 1: Buat Channel Baru
1. Buka Telegram
2. Buat **Channel** baru (bukan group)
3. Nama: "TGDrive Storage" atau terserah
4. Tipe: **Private** (untuk keamanan)
5. Deskripsi: "Storage channel untuk TGDrive"

## Langkah 2: Tambahkan Bot sebagai Admin
1. Di channel baru, klik nama channel → **Administrators**
2. Klik **Add Administrator** 
3. Cari **@Kudobot1bot**
4. Berikan semua permission:
   - ✅ Post Messages
   - ✅ Edit Messages
   - ✅ Delete Messages 
   - ✅ Pin Messages
   - ✅ Add Subscribers

## Langkah 3: Dapatkan Channel ID
1. Forward message apapun dari channel ke @userinfobot
2. Atau cek di web.telegram.org, lihat URL channel
3. Channel ID akan seperti: `-1001234567890`

## Langkah 4: Kirim Message Pertama
1. Di channel baru, kirim message:
   ```
   🔐 TGDrive Database Backup File
   
   File database akan diupload di sini secara otomatis.
   JANGAN HAPUS MESSAGE INI!
   ```
2. Ini akan jadi message ID 1

## Langkah 5: Update Environment
Buat file `.env` atau update yang ada:
```env
API_ID=24783879
API_HASH=935a8934034dfd64ecce5e9854fa071b
BOT_TOKENS=7914171749:AAHPJkVrKZKcvMLmg7A5UxtPpjUSOY2ezeI
STORAGE_CHANNEL=-1001234567890  # ← ID channel baru
DATABASE_BACKUP_MSG_ID=1         # ← Message pertama
DATABASE_BACKUP_TIME=60
WEBSITE_URL=http://209.74.81.235:8000
MAIN_BOT_TOKEN=7914171749:AAHPJkVrKZKcvMLmg7A5UxtPpjUSOY2ezeI
ADMIN_PASSWORD=123
TELEGRAM_ADMIN_IDS=7691463286,5381870056,5092392994,1841535556,1446366033,6137698413,5366835263
```

## Langkah 6: Clear Cache & Restart
```bash
rm -rf cache/
./deploy_fix.sh
```