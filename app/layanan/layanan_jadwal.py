from datetime import date, timedelta

from app.model.karyawan import Karyawan

NAMA_SHIFT = {
    "P": "Pagi",
    "S": "Siang",
    "M": "Malam",
    "L": "Libur",
}


def dapatkan_nama_shift(kode_shift: str) -> str:
    """Mengubah kode shift menjadi nama shift."""

    try:
        return NAMA_SHIFT[kode_shift]
    except KeyError as exc:
        raise ValueError(f"Kode shift tidak valid: {kode_shift}") from exc


def hitung_shift(karyawan: Karyawan, tanggal: date) -> str:
    """Menghitung kode shift karyawan pada tanggal tertentu."""

    if tanggal < karyawan.tanggal_mulai_kerja:
        raise ValueError("Jadwal tidak tersedia sebelum tanggal mulai kerja karyawan.")

    selisih_hari = (tanggal - karyawan.tanggal_acuan_siklus).days
    indeks_pola = selisih_hari % karyawan.panjang_siklus

    return karyawan.pola_shift[indeks_pola]


def buat_rentang_tanggal(
    tanggal_mulai: date,
    tanggal_selesai: date,
) -> list[date]:
    """Membuat daftar tanggal secara inklusif."""

    if tanggal_mulai > tanggal_selesai:
        raise ValueError("Tanggal mulai tidak boleh lebih besar dari tanggal selesai.")

    jumlah_hari = (tanggal_selesai - tanggal_mulai).days

    return [tanggal_mulai + timedelta(days=offset) for offset in range(jumlah_hari + 1)]


def buat_jadwal_karyawan(
    karyawan: Karyawan,
    tanggal_mulai: date,
    tanggal_selesai: date,
) -> list[dict[str, str]]:
    """Membuat jadwal karyawan dalam rentang tanggal."""

    rentang_tanggal = buat_rentang_tanggal(
        tanggal_mulai,
        tanggal_selesai,
    )

    jadwal = []

    for tanggal in rentang_tanggal:
        kode_shift = hitung_shift(karyawan, tanggal)

        jadwal.append(
            {
                "tanggal": tanggal.isoformat(),
                "hari": nama_hari(tanggal),
                "kode_shift": kode_shift,
                "nama_shift": dapatkan_nama_shift(kode_shift),
            }
        )

    return jadwal


def nama_hari(tanggal: date) -> str:
    """Menghasilkan nama hari dalam Bahasa Indonesia."""

    daftar_hari = (
        "Senin",
        "Selasa",
        "Rabu",
        "Kamis",
        "Jumat",
        "Sabtu",
        "Minggu",
    )

    return daftar_hari[tanggal.weekday()]
