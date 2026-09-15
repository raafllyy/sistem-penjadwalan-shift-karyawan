from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.basis_data.koneksi import dapatkan_sesi
from app.model.karyawan import Karyawan
from app.skema.karyawan import (
    DataKaryawan,
    ResponsDaftarKaryawan,
    ResponsDetailKaryawan,
)

router = APIRouter(
    prefix="/api/v1/karyawan",
    tags=["Karyawan"],
)

SesiBasisData = Annotated[Session, Depends(dapatkan_sesi)]


@router.get(
    "",
    response_model=ResponsDaftarKaryawan,
    summary="Ambil semua karyawan",
)
def ambil_semua_karyawan(
    sesi: SesiBasisData,
) -> ResponsDaftarKaryawan:
    """Mengambil seluruh data karyawan."""

    daftar_karyawan = sesi.scalars(
        select(Karyawan).order_by(Karyawan.kode_karyawan)
    ).all()

    return ResponsDaftarKaryawan(
        berhasil=True,
        jumlah=len(daftar_karyawan),
        data=[DataKaryawan.model_validate(karyawan) for karyawan in daftar_karyawan],
    )


@router.get(
    "/{kode_karyawan}",
    response_model=ResponsDetailKaryawan,
    summary="Ambil detail karyawan",
)
def ambil_detail_karyawan(
    kode_karyawan: str,
    sesi: SesiBasisData,
) -> ResponsDetailKaryawan:
    """Mengambil data karyawan berdasarkan kode."""

    karyawan = sesi.scalar(
        select(Karyawan).where(Karyawan.kode_karyawan == kode_karyawan)
    )

    if karyawan is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Karyawan tidak ditemukan.",
        )

    return ResponsDetailKaryawan(
        berhasil=True,
        data=DataKaryawan.model_validate(karyawan),
    )
