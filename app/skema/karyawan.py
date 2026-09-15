from datetime import date

from pydantic import BaseModel, ConfigDict


class DataKaryawan(BaseModel):
    """Representasi data karyawan pada respons API."""

    kode_karyawan: str
    nama: str
    pola_shift: list[str]
    panjang_siklus: int
    tanggal_mulai_kerja: date

    model_config = ConfigDict(from_attributes=True)


class ResponsDaftarKaryawan(BaseModel):
    """Respons daftar seluruh karyawan."""

    berhasil: bool
    jumlah: int
    data: list[DataKaryawan]


class ResponsDetailKaryawan(BaseModel):
    """Respons detail satu karyawan."""

    berhasil: bool
    data: DataKaryawan
