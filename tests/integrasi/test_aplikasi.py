from fastapi.testclient import TestClient

from app.main import aplikasi

klien = TestClient(aplikasi)


def test_aplikasi_berjalan() -> None:
    respons = klien.get("/")

    assert respons.status_code == 200
    assert respons.json()["berhasil"] is True


def test_status_kesehatan_aplikasi() -> None:
    respons = klien.get("/kesehatan")

    assert respons.status_code == 200

    data = respons.json()

    assert data["berhasil"] is True
    assert data["status"] == "sehat"
