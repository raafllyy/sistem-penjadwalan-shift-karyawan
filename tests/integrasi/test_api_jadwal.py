from fastapi.testclient import TestClient


def test_periksa_jadwal_ahmad(
    klien_api: TestClient,
) -> None:
    respons = klien_api.get(
        "/api/v1/jadwal/periksa",
        params={
            "kode_karyawan": "001",
            "tanggal": "2024-12-26",
        },
    )

    assert respons.status_code == 200

    data = respons.json()

    assert data["berhasil"] is True
    assert data["data"]["karyawan"]["nama"] == "Ahmad"
    assert data["data"]["hari"] == "Kamis"
    assert data["data"]["shift"]["kode"] == "S"
    assert data["data"]["shift"]["nama"] == "Siang"


def test_periksa_jadwal_karyawan_tidak_ditemukan(
    klien_api: TestClient,
) -> None:
    respons = klien_api.get(
        "/api/v1/jadwal/periksa",
        params={
            "kode_karyawan": "999",
            "tanggal": "2025-01-01",
        },
    )

    assert respons.status_code == 404


def test_periksa_jadwal_sebelum_mulai_kerja(
    klien_api: TestClient,
) -> None:
    respons = klien_api.get(
        "/api/v1/jadwal/periksa",
        params={
            "kode_karyawan": "001",
            "tanggal": "2024-12-25",
        },
    )

    data = respons.json()

    assert respons.status_code == 422
    assert data["berhasil"] is False
    assert (
        data["pesan"] == "Jadwal tidak tersedia sebelum tanggal mulai kerja karyawan."
    )


def test_format_tanggal_tidak_valid(
    klien_api: TestClient,
) -> None:
    respons = klien_api.get(
        "/api/v1/jadwal/periksa",
        params={
            "kode_karyawan": "001",
            "tanggal": "bukan-tanggal",
        },
    )

    assert respons.status_code == 422


def test_ambil_jadwal_semua_karyawan(
    klien_api: TestClient,
) -> None:
    respons = klien_api.get(
        "/api/v1/jadwal",
        params={
            "tanggal_mulai": "2024-12-26",
            "tanggal_selesai": "2024-12-29",
        },
    )

    assert respons.status_code == 200

    data = respons.json()

    assert data["berhasil"] is True
    assert data["meta"]["jumlah_hari"] == 4
    assert data["meta"]["jumlah_karyawan"] == 4
    assert len(data["data"]) == 4


def test_ambil_jadwal_satu_karyawan(
    klien_api: TestClient,
) -> None:
    respons = klien_api.get(
        "/api/v1/jadwal",
        params={
            "kode_karyawan": "001",
            "tanggal_mulai": "2024-12-26",
            "tanggal_selesai": "2024-12-30",
        },
    )

    assert respons.status_code == 200

    data = respons.json()

    assert data["meta"]["jumlah_hari"] == 5
    assert data["meta"]["jumlah_karyawan"] == 1

    assert len(data["data"]) == 1
    assert data["data"][0]["kode_karyawan"] == "001"
    assert data["data"][0]["nama"] == "Ahmad"


def test_jadwal_ahmad_dalam_rentang_tanggal(
    klien_api: TestClient,
) -> None:
    respons = klien_api.get(
        "/api/v1/jadwal",
        params={
            "kode_karyawan": "001",
            "tanggal_mulai": "2024-12-26",
            "tanggal_selesai": "2024-12-30",
        },
    )

    assert respons.status_code == 200

    jadwal = respons.json()["data"][0]["jadwal"]

    assert [item["kode_shift"] for item in jadwal] == [
        "S",
        "M",
        "M",
        "L",
        "P",
    ]


def test_rentang_jadwal_bersifat_inklusif(
    klien_api: TestClient,
) -> None:
    respons = klien_api.get(
        "/api/v1/jadwal",
        params={
            "kode_karyawan": "001",
            "tanggal_mulai": "2025-01-01",
            "tanggal_selesai": "2025-01-01",
        },
    )

    assert respons.status_code == 200

    data = respons.json()

    assert data["meta"]["jumlah_hari"] == 1
    assert len(data["data"][0]["jadwal"]) == 1


def test_rentang_tanggal_tidak_valid(
    klien_api: TestClient,
) -> None:
    respons = klien_api.get(
        "/api/v1/jadwal",
        params={
            "tanggal_mulai": "2025-01-10",
            "tanggal_selesai": "2025-01-01",
        },
    )

    data = respons.json()

    assert respons.status_code == 422
    assert data["berhasil"] is False
    assert (
        data["pesan"] == "Tanggal mulai tidak boleh lebih besar dari tanggal selesai."
    )


def test_filter_karyawan_tidak_ditemukan(
    klien_api: TestClient,
) -> None:
    respons = klien_api.get(
        "/api/v1/jadwal",
        params={
            "kode_karyawan": "999",
            "tanggal_mulai": "2025-01-01",
            "tanggal_selesai": "2025-01-05",
        },
    )

    data = respons.json()

    assert respons.status_code == 404
    assert data["berhasil"] is False
    assert data["pesan"] == "Karyawan tidak ditemukan."


def test_jadwal_sebelum_tanggal_mulai_kerja_ditolak(
    klien_api: TestClient,
) -> None:
    respons = klien_api.get(
        "/api/v1/jadwal",
        params={
            "tanggal_mulai": "2024-12-25",
            "tanggal_selesai": "2024-12-29",
        },
    )

    data = respons.json()

    assert respons.status_code == 422
    assert data["berhasil"] is False
    assert (
        data["pesan"] == "Jadwal tidak tersedia sebelum tanggal mulai kerja karyawan."
    )
