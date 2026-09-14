from fastapi import FastAPI

from app.inti.konfigurasi import konfigurasi

aplikasi = FastAPI(
    title=konfigurasi.nama_aplikasi,
    version=konfigurasi.versi_aplikasi,
    description=(
        "API untuk menghitung dan menampilkan jadwal shift karyawan "
        "berdasarkan pola kerja berulang."
    ),
    debug=konfigurasi.mode_debug,
)

@aplikasi.get(
    "/",
    tags=["Sistem"],
    summary="Informasi aplikasi",
)
def informasi_aplikasi() -> dict:
    """Menampilkan informasi dasar aplikasi."""

    return {
        "berhasil": True,
        "pesan": "Sistem Penjadwalan Shift Karyawan berjalan.",
        "versi": konfigurasi.versi_aplikasi,
    }

@aplikasi.get(
    "/kesehatan",
    tags=["Sistem"],
    summary="Periksa kesehatan aplikasi",
)
def periksa_kesehatan() -> dict:
    """Memastikan aplikasi dapat menerima permintaan."""

    return {
        "berhasil": True,
        "status": "sehat",
    }