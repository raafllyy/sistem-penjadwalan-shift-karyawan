from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.basis_data.koneksi import dapatkan_sesi
from app.layanan.layanan_jadwal import (
    buat_jadwal_karyawan,
    buat_rentang_tanggal,
    dapatkan_nama_shift,
    hitung_shift,
    nama_hari,
)
from app.model.karyawan import Karyawan
from app.skema.jadwal import (
    DataJadwalHarian,
    DataJadwalKaryawan,
    DataKaryawanJadwal,
    DataPeriksaJadwal,
    DataShift,
    MetaJadwal,
    ResponsDaftarJadwal,
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


@router.get(
    "",
    response_model=ResponsDaftarJadwal,
    summary="Ambil jadwal karyawan",
)
def ambil_jadwal(
    sesi: SesiBasisData,
    tanggal_mulai: Annotated[
        date,
        Query(
            description="Tanggal awal jadwal dengan format YYYY-MM-DD.",
        ),
    ],
    tanggal_selesai: Annotated[
        date,
        Query(
            description="Tanggal akhir jadwal dengan format YYYY-MM-DD.",
        ),
    ],
    kode_karyawan: Annotated[
        str | None,
        Query(
            min_length=1,
            description=(
                "Kode karyawan. Kosongkan untuk menampilkan seluruh karyawan."
            ),
        ),
    ] = None,
) -> ResponsDaftarJadwal:
    """Mengambil jadwal semua atau satu karyawan dalam rentang tanggal."""

    try:
        rentang_tanggal = buat_rentang_tanggal(
            tanggal_mulai,
            tanggal_selesai,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc

    pernyataan = select(Karyawan).order_by(Karyawan.kode_karyawan)

    if kode_karyawan is not None:
        pernyataan = pernyataan.where(Karyawan.kode_karyawan == kode_karyawan)

    daftar_karyawan = sesi.scalars(pernyataan).all()

    if kode_karyawan is not None and not daftar_karyawan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Karyawan tidak ditemukan.",
        )

    data_jadwal: list[DataJadwalKaryawan] = []

    try:
        for karyawan in daftar_karyawan:
            hasil_jadwal = buat_jadwal_karyawan(
                karyawan,
                tanggal_mulai,
                tanggal_selesai,
            )

            data_jadwal.append(
                DataJadwalKaryawan(
                    kode_karyawan=karyawan.kode_karyawan,
                    nama=karyawan.nama,
                    jadwal=[DataJadwalHarian(**item) for item in hasil_jadwal],
                )
            )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc

    return ResponsDaftarJadwal(
        berhasil=True,
        meta=MetaJadwal(
            tanggal_mulai=tanggal_mulai,
            tanggal_selesai=tanggal_selesai,
            jumlah_hari=len(rentang_tanggal),
            jumlah_karyawan=len(daftar_karyawan),
        ),
        data=data_jadwal,
    )
