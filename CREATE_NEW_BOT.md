# 🤖 Cara Buat Bot Token Baru (2 menit)

## Langkah Cepat:

### 1. Buka @BotFather di Telegram
- Ketik `/start`
- Ketik `/newbot`

### 2. Isi Detail Bot
- **Bot name:** `YourName Drive Bot V2` (atau apapun)
- **Bot username:** `yournamedrivebot2` (harus unik, akhiri dengan 'bot')

### 3. Copy Token Baru
BotFather akan berikan token seperti:
```
7123456789:AAGxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 4. Update .env
Ganti BOT_TOKENS dan MAIN_BOT_TOKEN dengan token baru

### 5. Tambahkan Bot Baru ke Channel
- Buka channel `-1002678381463`
- Hapus bot lama @Kudobot4bot 
- Tambahkan bot baru sebagai admin
- Berikan semua permission

### 6. Restart TGDrive
```bash
rm -rf cache/
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000
```

## ⚡ Keuntungan:
- ✅ Bypass flood wait instantly
- ✅ Fresh bot, no rate limit
- ✅ Clean start

## 💡 Tips:
- Simpan token lama untuk backup
- Jangan spam restart bot untuk avoid flood wait