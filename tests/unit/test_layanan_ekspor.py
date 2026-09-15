import csv
from datetime import date
from io import BytesIO, StringIO

from openpyxl import load_workbook

from app.layanan.layanan_ekspor import (
    buat_csv,
    buat_excel,
    buat_matriks_jadwal,
)
from app.model.karyawan import Karyawan


def buat_ahmad() -> Karyawan:
    """Membuat data Ahmad untuk pengujian."""

    return Karyawan(
        kode_karyawan="001",
        nama="Ahmad",
        pola_shift=["P", "P", "S", "S", "M", "M", "L"],
        panjang_siklus=7,
        tanggal_mulai_kerja=date(2024, 12, 26),
        tanggal_acuan_siklus=date(2024, 12, 23),
    )


def test_buat_matriks_jadwal() -> None:
    header, baris = buat_matriks_jadwal(
        [buat_ahmad()],
        date(2024, 12, 26),
        date(2024, 12, 29),
    )

    assert header == [
        "ID",
        "Nama",
        "2024/12/26",
        "2024/12/27",
        "2024/12/28",
        "2024/12/29",
    ]

    assert baris == [
        [
            "001",
            "Ahmad",
            "S",
            "M",
            "M",
            "L",
        ]
    ]


def test_buat_csv() -> None:
    isi_file = buat_csv(
        [buat_ahmad()],
        date(2024, 12, 26),
        date(2024, 12, 29),
    )

    teks = isi_file.decode("utf-8-sig")

    pembaca = csv.reader(StringIO(teks))
    baris = list(pembaca)

    assert baris[0] == [
        "ID",
        "Nama",
        "2024/12/26",
        "2024/12/27",
        "2024/12/28",
        "2024/12/29",
    ]

    assert baris[1] == [
        "001",
        "Ahmad",
        "S",
        "M",
        "M",
        "L",
    ]


def test_buat_excel() -> None:
    isi_file = buat_excel(
        [buat_ahmad()],
        date(2024, 12, 26),
        date(2024, 12, 29),
    )

    workbook = load_workbook(BytesIO(isi_file))
    worksheet = workbook["Jadwal Shift"]

    assert worksheet["A1"].value == "ID"
    assert worksheet["B1"].value == "Nama"
    assert worksheet["C1"].value == "2024/12/26"
    assert worksheet["F1"].value == "2024/12/29"

    assert worksheet["A2"].value == "001"
    assert worksheet["B2"].value == "Ahmad"
    assert worksheet["C2"].value == "S"
    assert worksheet["D2"].value == "M"
    assert worksheet["E2"].value == "M"
    assert worksheet["F2"].value == "L"

    workbook.close()
