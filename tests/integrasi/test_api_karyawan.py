from fastapi.testclient import TestClient


def test_ambil_semua_karyawan(
    klien_api: TestClient,
) -> None:
    respons = klien_api.get("/api/v1/karyawan")

    assert respons.status_code == 200

    data = respons.json()

    assert data["berhasil"] is True
    assert data["jumlah"] == 4
    assert len(data["data"]) == 4


def test_ambil_detail_karyawan(
    klien_api: TestClient,
) -> None:
    respons = klien_api.get("/api/v1/karyawan/001")

    assert respons.status_code == 200

    data = respons.json()

    assert data["berhasil"] is True
    assert data["data"]["kode_karyawan"] == "001"
    assert data["data"]["nama"] == "Ahmad"


def test_karyawan_tidak_ditemukan(
    klien_api: TestClient,
) -> None:
    respons = klien_api.get("/api/v1/karyawan/999")

    data = respons.json()

    assert respons.status_code == 404
    assert data["berhasil"] is False
    assert data["pesan"] == "Karyawan tidak ditemukan."
