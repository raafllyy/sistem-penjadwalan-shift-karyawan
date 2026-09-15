from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.ekspor import router as router_ekspor
from app.api.jadwal import router as router_jadwal
from app.api.karyawan import router as router_karyawan
from app.basis_data.seed import inisialisasi_basis_data
from app.inti.konfigurasi import konfigurasi


@asynccontextmanager
async def siklus_hidup(_: FastAPI) -> AsyncIterator[None]:
    """Menyiapkan sumber daya aplikasi saat mulai dijalankan."""

    inisialisasi_basis_data()

    yield


aplikasi = FastAPI(
    title=konfigurasi.nama_aplikasi,
    version=konfigurasi.versi_aplikasi,
    description=(
        "API untuk menghitung dan menampilkan jadwal shift karyawan "
        "berdasarkan pola kerja berulang."
    ),
    debug=konfigurasi.mode_debug,
    lifespan=siklus_hidup,
)

aplikasi.include_router(router_karyawan)
aplikasi.include_router(router_jadwal)
aplikasi.include_router(router_ekspor)


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
