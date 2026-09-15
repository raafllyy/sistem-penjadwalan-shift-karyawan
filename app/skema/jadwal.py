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


class DataJadwalHarian(BaseModel):
    """Informasi jadwal pada satu tanggal."""

    tanggal: date
    hari: str
    kode_shift: str
    nama_shift: str


class DataJadwalKaryawan(BaseModel):
    """Jadwal seorang karyawan dalam rentang tanggal."""

    kode_karyawan: str
    nama: str
    jadwal: list[DataJadwalHarian]


class MetaJadwal(BaseModel):
    """Metadata rentang jadwal."""

    tanggal_mulai: date
    tanggal_selesai: date
    jumlah_hari: int
    jumlah_karyawan: int


class ResponsDaftarJadwal(BaseModel):
    """Respons jadwal karyawan berdasarkan rentang tanggal."""

    berhasil: bool
    meta: MetaJadwal
    data: list[DataJadwalKaryawan]
