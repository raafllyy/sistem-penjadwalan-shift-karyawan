from datetime import date
from io import BytesIO
from typing import Annotated, Literal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import StreamingResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.basis_data.koneksi import dapatkan_sesi
from app.layanan.layanan_ekspor import buat_csv, buat_excel
from app.model.karyawan import Karyawan

router = APIRouter(
    prefix="/api/v1/jadwal",
    tags=["Ekspor"],
)

SesiBasisData = Annotated[Session, Depends(dapatkan_sesi)]


@router.get(
    "/ekspor",
    summary="Ekspor jadwal karyawan",
)
def ekspor_jadwal(
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
    format_ekspor: Annotated[
        Literal["csv", "xlsx"],
        Query(
            alias="format",
            description="Format file yang akan dihasilkan.",
        ),
    ] = "xlsx",
    kode_karyawan: Annotated[
        str | None,
        Query(
            min_length=1,
            description=("Kode karyawan. Kosongkan untuk mengekspor seluruh karyawan."),
        ),
    ] = None,
) -> StreamingResponse:
    """Mengekspor jadwal semua atau satu karyawan."""

    if tanggal_mulai > tanggal_selesai:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=("Tanggal mulai tidak boleh lebih besar dari tanggal selesai."),
        )

    pernyataan = select(Karyawan).order_by(Karyawan.kode_karyawan)

    if kode_karyawan is not None:
        pernyataan = pernyataan.where(Karyawan.kode_karyawan == kode_karyawan)

    daftar_karyawan = sesi.scalars(pernyataan).all()

    if kode_karyawan is not None and not daftar_karyawan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Karyawan tidak ditemukan.",
        )

    try:
        if format_ekspor == "csv":
            isi_file = buat_csv(
                daftar_karyawan,
                tanggal_mulai,
                tanggal_selesai,
            )

            tipe_media = "text/csv; charset=utf-8"
            ekstensi = "csv"

        else:
            isi_file = buat_excel(
                daftar_karyawan,
                tanggal_mulai,
                tanggal_selesai,
            )

            tipe_media = (
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            ekstensi = "xlsx"

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc

    nama_file = (
        f"jadwal-shift-{tanggal_mulai.isoformat()}"
        f"-sampai-{tanggal_selesai.isoformat()}.{ekstensi}"
    )

    return StreamingResponse(
        BytesIO(isi_file),
        media_type=tipe_media,
        headers={"Content-Disposition": (f'attachment; filename="{nama_file}"')},
    )
