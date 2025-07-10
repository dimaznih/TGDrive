# Fix Channel yang Ada

## Langkah 1: Tambahkan Bot ke Channel
1. Buka Telegram, cari channel dengan ID `-1002843656111`
2. Klik nama channel → **Administrators** 
3. Klik **Add Administrator**
4. Cari bot **@Kudobot1bot**
5. Berikan permission:
   - ✅ Post Messages
   - ✅ Edit Messages  
   - ✅ Delete Messages
   - ✅ Pin Messages

## Langkah 2: Buat Message Backup Awal
1. Di channel tersebut, kirim message:
   ```
   🔐 TGDrive Database Backup
   
   Jangan hapus message ini!
   ```
2. Catat message ID nya (biasanya muncul di URL atau bisa dilihat dengan forward ke @userinfobot)

## Langkah 3: Update Environment 
Update `DATABASE_BACKUP_MSG_ID` sesuai message yang baru dibuat:
```env
DATABASE_BACKUP_MSG_ID=<message_id_yang_baru>
```

## Langkah 4: Restart
```bash
./deploy_fix.sh
```