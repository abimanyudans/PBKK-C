# Fraud Detection System - Deployment Guide

## Deploy ke Render.com

### Langkah 1: Persiapan Repository

1. Push semua perubahan ke GitHub:
   ```bash
   git add .
   git commit -m "Prepare for Render deployment"
   git push origin master
   ```

### Langkah 2: Buat Akun Render

1. Buka [render.com](https://render.com)
2. Sign up dengan akun GitHub Anda
3. Authorize Render untuk akses repository

### Langkah 3: Deploy Web Service

1. Di Render dashboard, klik **"New +"** → **"Web Service"**
2. Connect repository GitHub Anda: `fraud-detection-web-app-with-flask`
3. Isi konfigurasi:

   - **Name**: `fraud-detection-system` (atau nama lain)
   - **Region**: Singapore (terdekat dengan Indonesia)
   - **Branch**: `master`
   - **Root Directory**: `Credit-Card-Fraud-Detection-System`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Instance Type**: `Free`

4. Klik **"Create Web Service"**

### Langkah 4: Tunggu Deploy

- Render akan otomatis build dan deploy
- Proses biasanya 5-10 menit
- Anda akan dapat URL seperti: `https://fraud-detection-system.onrender.com`

### Catatan Penting:

- ✅ Free tier Render akan sleep setelah 15 menit tidak aktif
- ✅ Pertama kali diakses akan lambat (cold start ~30 detik)
- ✅ ML models akan di-load otomatis dari folder `ml model/`
- ✅ Dataset akan di-load dari folder `dataset/`

### Troubleshooting:

Jika ada error saat build:

1. Check logs di Render dashboard
2. Pastikan semua file ML model sudah di-push ke GitHub
3. Pastikan `requirements.txt` sesuai dengan versi Python di Render

### Alternative: Manual Deploy (jika render.yaml tidak terdeteksi)

Gunakan konfigurasi manual di Render dashboard seperti di langkah 3.

---

**Selamat! Aplikasi Anda akan live di internet! 🚀**
