from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.basis_data.koneksi import dapatkan_sesi
from app.layanan.layanan_jadwal import (
    dapatkan_nama_shift,
    hitung_shift,
    nama_hari,
)
from app.model.karyawan import Karyawan
from app.skema.jadwal import (
    DataKaryawanJadwal,
    DataPeriksaJadwal,
    DataShift,
    ResponsPeriksaJadwal,
)

router = APIRouter(
    prefix="/api/v1/jadwal",
    tags=["Jadwal"],
)

SesiBasisData = Annotated[Session, Depends(dapatkan_sesi)]


@router.get(
    "/periksa",
    response_model=ResponsPeriksaJadwal,
    summary="Periksa jadwal karyawan",
)
def periksa_jadwal(
    sesi: SesiBasisData,
    kode_karyawan: Annotated[
        str,
        Query(
            min_length=1,
            description="Kode karyawan yang akan diperiksa.",
        ),
    ],
    tanggal: Annotated[
        date,
        Query(
            description="Tanggal yang diperiksa dengan format YYYY-MM-DD.",
        ),
    ],
) -> ResponsPeriksaJadwal:
    """Memeriksa shift seorang karyawan pada tanggal tertentu."""

    karyawan = sesi.scalar(
        select(Karyawan).where(Karyawan.kode_karyawan == kode_karyawan)
    )

    if karyawan is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Karyawan tidak ditemukan.",
        )

    try:
        kode_shift = hitung_shift(karyawan, tanggal)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc

    return ResponsPeriksaJadwal(
        berhasil=True,
        data=DataPeriksaJadwal(
            karyawan=DataKaryawanJadwal(
                kode=karyawan.kode_karyawan,
                nama=karyawan.nama,
            ),
            tanggal=tanggal,
            hari=nama_hari(tanggal),
            shift=DataShift(
                kode=kode_shift,
                nama=dapatkan_nama_shift(kode_shift),
            ),
        ),
    )
