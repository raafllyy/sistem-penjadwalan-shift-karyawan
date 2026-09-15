from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.basis_data.koneksi import BasisModel, SesiLokal, engine
from app.model.karyawan import Karyawan

DATA_KARYAWAN = (
    {
        "kode_karyawan": "001",
        "nama": "Ahmad",
        "pola_shift": ["P", "P", "S", "S", "M", "M", "L"],
        "panjang_siklus": 7,
        "tanggal_mulai_kerja": date(2024, 12, 26),
        "tanggal_acuan_siklus": date(2024, 12, 23),
    },
    {
        "kode_karyawan": "002",
        "nama": "Widi",
        "pola_shift": ["S", "S", "M", "M", "L", "P", "S"],
        "panjang_siklus": 7,
        "tanggal_mulai_kerja": date(2024, 12, 26),
        "tanggal_acuan_siklus": date(2024, 12, 23),
    },
    {
        "kode_karyawan": "003",
        "nama": "Yono",
        "pola_shift": ["M", "M", "P", "L", "P", "P", "M"],
        "panjang_siklus": 7,
        "tanggal_mulai_kerja": date(2024, 12, 26),
        "tanggal_acuan_siklus": date(2024, 12, 23),
    },
    {
        "kode_karyawan": "004",
        "nama": "Yohan",
        "pola_shift": [
            "L",
            "P",
            "P",
            "P",
            "S",
            "S",
            "P",
            "L",
            "S",
            "S",
            "P",
            "S",
            "S",
            "P",
        ],
        "panjang_siklus": 14,
        "tanggal_mulai_kerja": date(2024, 12, 26),
        "tanggal_acuan_siklus": date(2024, 12, 23),
    },
)


def seed_karyawan(sesi: Session) -> None:
    """Menambahkan data awal karyawan yang belum tersedia."""

    kode_tersedia = set(sesi.scalars(select(Karyawan.kode_karyawan)).all())

    karyawan_baru = [
        Karyawan(**data)
        for data in DATA_KARYAWAN
        if data["kode_karyawan"] not in kode_tersedia
    ]

    if not karyawan_baru:
        return

    sesi.add_all(karyawan_baru)
    sesi.commit()


def inisialisasi_basis_data() -> None:
    """Membuat tabel dan mengisi data awal aplikasi."""

    BasisModel.metadata.create_all(bind=engine)

    with SesiLokal() as sesi:
        seed_karyawan(sesi)
