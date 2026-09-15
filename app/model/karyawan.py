from datetime import date, datetime

from sqlalchemy import JSON, Date, DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.basis_data.koneksi import BasisModel


class Karyawan(BasisModel):
    """Model data karyawan dan pola shift."""

    __tablename__ = "karyawan"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    kode_karyawan: Mapped[str] = mapped_column(
        String(10),
        unique=True,
        index=True,
        nullable=False,
    )

    nama: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    pola_shift: Mapped[list[str]] = mapped_column(
        JSON,
        nullable=False,
    )

    panjang_siklus: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    tanggal_mulai_kerja: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    tanggal_acuan_siklus: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    dibuat_pada: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False,
    )

    diperbarui_pada: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"Karyawan(kode_karyawan={self.kode_karyawan!r}, nama={self.nama!r})"
