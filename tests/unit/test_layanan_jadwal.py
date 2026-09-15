from datetime import date

import pytest

from app.layanan.layanan_jadwal import (
    buat_jadwal_karyawan,
    buat_rentang_tanggal,
    dapatkan_nama_shift,
    hitung_shift,
    nama_hari,
)
from app.model.karyawan import Karyawan


def buat_karyawan(
    kode: str,
    nama: str,
    pola_shift: list[str],
) -> Karyawan:
    """Membuat objek karyawan untuk kebutuhan pengujian."""

    return Karyawan(
        kode_karyawan=kode,
        nama=nama,
        pola_shift=pola_shift,
        panjang_siklus=len(pola_shift),
        tanggal_mulai_kerja=date(2024, 12, 26),
        tanggal_acuan_siklus=date(2024, 12, 23),
    )


@pytest.fixture
def ahmad() -> Karyawan:
    return buat_karyawan(
        "001",
        "Ahmad",
        ["P", "P", "S", "S", "M", "M", "L"],
    )


@pytest.fixture
def widi() -> Karyawan:
    return buat_karyawan(
        "002",
        "Widi",
        ["S", "S", "M", "M", "L", "P", "S"],
    )


@pytest.fixture
def yono() -> Karyawan:
    return buat_karyawan(
        "003",
        "Yono",
        ["M", "M", "P", "L", "P", "P", "M"],
    )


@pytest.fixture
def yohan() -> Karyawan:
    return buat_karyawan(
        "004",
        "Yohan",
        [
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
    )


def test_shift_ahmad_pada_tanggal_mulai(
    ahmad: Karyawan,
) -> None:
    assert hitung_shift(ahmad, date(2024, 12, 26)) == "S"


def test_shift_widi_pada_tanggal_mulai(
    widi: Karyawan,
) -> None:
    assert hitung_shift(widi, date(2024, 12, 26)) == "M"


def test_shift_yono_pada_tanggal_mulai(
    yono: Karyawan,
) -> None:
    assert hitung_shift(yono, date(2024, 12, 26)) == "L"


def test_shift_yohan_pada_tanggal_mulai(
    yohan: Karyawan,
) -> None:
    assert hitung_shift(yohan, date(2024, 12, 26)) == "P"


def test_siklus_ahmad_berulang_setelah_tujuh_hari(
    ahmad: Karyawan,
) -> None:
    tanggal = date(2025, 1, 6)

    assert hitung_shift(ahmad, tanggal) == hitung_shift(
        ahmad,
        date(2025, 1, 13),
    )


def test_siklus_widi_berulang_setelah_tujuh_hari(
    widi: Karyawan,
) -> None:
    tanggal = date(2025, 1, 6)

    assert hitung_shift(widi, tanggal) == hitung_shift(
        widi,
        date(2025, 1, 13),
    )


def test_siklus_yono_berulang_setelah_tujuh_hari(
    yono: Karyawan,
) -> None:
    tanggal = date(2025, 1, 6)

    assert hitung_shift(yono, tanggal) == hitung_shift(
        yono,
        date(2025, 1, 13),
    )


def test_siklus_yohan_berulang_setelah_empat_belas_hari(
    yohan: Karyawan,
) -> None:
    tanggal = date(2025, 1, 6)

    assert hitung_shift(yohan, tanggal) == hitung_shift(
        yohan,
        date(2025, 1, 20),
    )


def test_tanggal_sebelum_mulai_kerja_ditolak(
    ahmad: Karyawan,
) -> None:
    with pytest.raises(
        ValueError,
        match="Jadwal tidak tersedia",
    ):
        hitung_shift(ahmad, date(2024, 12, 25))


def test_rentang_tanggal_bersifat_inklusif() -> None:
    hasil = buat_rentang_tanggal(
        date(2025, 1, 1),
        date(2025, 1, 3),
    )

    assert hasil == [
        date(2025, 1, 1),
        date(2025, 1, 2),
        date(2025, 1, 3),
    ]


def test_rentang_tanggal_tidak_valid_ditolak() -> None:
    with pytest.raises(
        ValueError,
        match="Tanggal mulai tidak boleh",
    ):
        buat_rentang_tanggal(
            date(2025, 1, 10),
            date(2025, 1, 1),
        )


def test_nama_hari_menggunakan_bahasa_indonesia() -> None:
    assert nama_hari(date(2025, 1, 6)) == "Senin"
    assert nama_hari(date(2025, 1, 12)) == "Minggu"


def test_nama_shift_sesuai() -> None:
    assert dapatkan_nama_shift("P") == "Pagi"
    assert dapatkan_nama_shift("S") == "Siang"
    assert dapatkan_nama_shift("M") == "Malam"
    assert dapatkan_nama_shift("L") == "Libur"


def test_kode_shift_tidak_valid_ditolak() -> None:
    with pytest.raises(
        ValueError,
        match="Kode shift tidak valid",
    ):
        dapatkan_nama_shift("X")


def test_buat_jadwal_karyawan(
    ahmad: Karyawan,
) -> None:
    hasil = buat_jadwal_karyawan(
        ahmad,
        date(2024, 12, 26),
        date(2024, 12, 29),
    )

    assert len(hasil) == 4

    assert hasil[0] == {
        "tanggal": "2024-12-26",
        "hari": "Kamis",
        "kode_shift": "S",
        "nama_shift": "Siang",
    }

    assert hasil[-1] == {
        "tanggal": "2024-12-29",
        "hari": "Minggu",
        "kode_shift": "L",
        "nama_shift": "Libur",
    }
