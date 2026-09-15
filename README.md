# Sistem Penjadwalan Shift Karyawan

Aplikasi berbasis FastAPI untuk menghitung jadwal kerja karyawan berdasarkan pola shift berulang.

Fitur utama:
- Cek Shift Harian — melihat shift satu atau seluruh karyawan pada tanggal tertentu.
- Jadwal Rentang Tanggal** — melihat jadwal satu atau seluruh karyawan pada periode tertentu.
- Ekspor Jadwal — mengunduh jadwal dalam format CSV atau Excel (`.xlsx`).
- Antarmuka Web — tersedia pada `/aplikasi`.
- REST API — dilengkapi Swagger, pengujian Pytest, serta Postman/Newman.

## Teknologi

Python, FastAPI, Uvicorn, SQLAlchemy, SQLite, Pydantic, Jinja2, HTML, CSS, JavaScript, openpyxl, pytest, Ruff, Postman, dan Newman.

# Instalasi

## 1. Prasyarat

Pastikan komputer sudah memiliki:

- Python 3.12+
- Git

Opsional:
- Visual Studio Code
- Node.js, hanya diperlukan untuk menjalankan Newman

Cek instalasi melalui terminal:
    python --version
    git --version

Jika perintah `python` tidak tersedia, coba:
    py --version

## 2. Ambil Project

Jalankan di terminal:
    git clone (https://github.com/raafllyy/sistem-penjadwalan-shift-karyawan)
    
    cd sistem-penjadwalan-shift-karyawan

Jika project diperoleh melalui ZIP, extract terlebih dahulu lalu buka terminal pada folder project.

## 3. Buat Virtual Environment

Jalankan:
    python -m venv venv

Aktifkan:
    .\venv\Scripts\Activate.ps1

Jika berhasil, terminal akan diawali dengan:
    (venv)

Jika terminal/powershell menolak aktivasi:
    Set-ExecutionPolicy -Scope CurrentUser RemoteSigned

Kemudian aktifkan kembali virtual environment.

## 4. Install Dependency

Untuk menjalankan aplikasi:
    python -m pip install --upgrade pip
    pip install -r requirements.txt

Untuk development, testing, dan Ruff:
    pip install -r requirements-dev.txt

## 5. Siapkan Environment

Salin `.env.example` menjadi `.env`:
    Copy-Item .env.example .env


Konfigurasi default:
    env
        NAMA_APLIKASI="Sistem Penjadwalan Shift Karyawan"
        VERSI_APLIKASI="1.0.0"
        MODE_DEBUG=true
        URL_BASIS_DATA="sqlite:///./database.sqlite3"

Database SQLite dan data awal karyawan akan dibuat otomatis saat aplikasi pertama kali dijalankan.

## 6. Jalankan Aplikasi

Jalankan di Terminal:
    uvicorn app.main:aplikasi --reload

Jika berhasil, server berjalan pada:
    http://127.0.0.1:8000

Biarkan terminal tetap terbuka selama aplikasi digunakan.

## 7. Buka Aplikasi

Buka alamat berikut melalui browser, bukan terminal:
    http://127.0.0.1:8000/aplikasi

Antarmuka web dapat digunakan untuk:
- mengecek shift harian;
- melihat jadwal berdasarkan rentang tanggal;
- memilih satu atau seluruh karyawan;
- mengekspor jadwal ke CSV atau Excel.

# URL Penting

 Antarmuka Web  `http://127.0.0.1:8000/aplikasi` 
 Informasi API  `http://127.0.0.1:8000/` 
 Swagger  `http://127.0.0.1:8000/docs` 
 ReDoc  `http://127.0.0.1:8000/redoc` 

# Pengujian

Pastikan virtual environment aktif.

Jalankan seluruh test:
    pytest

Periksa format dan kualitas kode:
    ruff format .
    ruff check .

# Pengujian API dengan Newman

Bagian ini opsional. Pastikan Node.js sudah terpasang.

Install dependency Node.js:
    npm ci

Jalankan FastAPI pada terminal pertama - 1:
    uvicorn app.main:aplikasi --reload

Kemudian buka terminal kedua - 2 dan jalankan:
    npm run uji:api

Target pengujian adalah seluruh request dan assertion selesai dengan `0 failed`.

# Troubleshooting

### Port 8000 sudah digunakan

Gunakan port lain:
    uvicorn app.main:aplikasi --reload --port 8001

Lalu buka di browser:
    http://127.0.0.1:8001/aplikasi

### Module tidak ditemukan

Pastikan terminal menampilkan `(venv)`, kemudian jalankan:
    pip install -r requirements.txt

### Membuat ulang database

Matikan server, lalu hapus database:
    Remove-Item database.sqlite3

Jalankan aplikasi kembali. Database dan data awal akan dibuat otomatis.

# Instalasi Cepat

Jalankan seluruh perintah berikut di Terminal:
    git clone <URL_REPOSITORY_GITHUB>
    cd sistem-penjadwalan-shift-karyawan
    python -m venv venv
    .\venv\Scripts\Activate.ps1
    pip install -r requirements.txt
    Copy-Item .env.example .env
    uvicorn app.main:aplikasi --reload

Setelah server berjalan, buka melalui browser:
http://127.0.0.1:8000/aplikasi

# Dokumentasi Postman
    https://documenter.getpostman.com/view/52143051/2sBYAyuUsN
