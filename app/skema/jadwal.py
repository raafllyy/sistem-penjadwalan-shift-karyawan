from datetime import date

from pydantic import BaseModel


class DataKaryawanJadwal(BaseModel):
    """Identitas singkat karyawan pada jadwal."""

    kode: str
    nama: str


class DataShift(BaseModel):
    """Informasi shift karyawan."""

    kode: str
    nama: str


class DataPeriksaJadwal(BaseModel):
    """Hasil pemeriksaan jadwal satu karyawan."""

    karyawan: DataKaryawanJadwal
    tanggal: date
    hari: str
    shift: DataShift


class ResponsPeriksaJadwal(BaseModel):
    """Respons pemeriksaan jadwal karyawan."""

    berhasil: bool
    data: DataPeriksaJadwal
