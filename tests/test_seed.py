from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.basis_data.koneksi import BasisModel
from app.basis_data.seed import seed_karyawan
from app.model.karyawan import Karyawan


def buat_sesi_pengujian() -> Session:
    """Membuat basis data SQLite sementara untuk pengujian."""

    engine_pengujian = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    BasisModel.metadata.create_all(bind=engine_pengujian)

    return Session(engine_pengujian)


def test_seed_menambahkan_empat_karyawan() -> None:
    sesi = buat_sesi_pengujian()

    try:
        seed_karyawan(sesi)

        jumlah_karyawan = sesi.scalar(select(func.count()).select_from(Karyawan))

        assert jumlah_karyawan == 4
    finally:
        sesi.close()


def test_seed_tidak_menggandakan_data() -> None:
    sesi = buat_sesi_pengujian()

    try:
        seed_karyawan(sesi)
        seed_karyawan(sesi)

        jumlah_karyawan = sesi.scalar(select(func.count()).select_from(Karyawan))

        assert jumlah_karyawan == 4
    finally:
        sesi.close()


def test_seed_memiliki_kode_karyawan_yang_benar() -> None:
    sesi = buat_sesi_pengujian()

    try:
        seed_karyawan(sesi)

        daftar_kode = sesi.scalars(
            select(Karyawan.kode_karyawan).order_by(Karyawan.kode_karyawan)
        ).all()

        assert len(daftar_kode) == 4
        assert len(set(daftar_kode)) == 4
        assert all(kode for kode in daftar_kode)
    finally:
        sesi.close()
