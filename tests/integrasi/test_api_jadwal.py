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

    assert respons.status_code == 422

    assert (
        respons.json()["detail"]
        == "Jadwal tidak tersedia sebelum tanggal mulai kerja karyawan."
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
