from fastapi.testclient import TestClient


def test_halaman_dapat_diakses(
    klien_api: TestClient,
) -> None:
    respons = klien_api.get("/aplikasi")

    assert respons.status_code == 200
    assert "Sistem Penjadwalan Shift Karyawan" in respons.text


def test_halaman_memiliki_form_periksa_shift(
    klien_api: TestClient,
) -> None:
    respons = klien_api.get("/aplikasi")

    assert respons.status_code == 200
    assert 'id="form-periksa"' in respons.text
    assert "Cek Shift Harian" in respons.text
    assert 'id="periksa-karyawan"' in respons.text
    assert 'id="periksa-tanggal"' in respons.text


def test_halaman_memiliki_form_rentang_jadwal(
    klien_api: TestClient,
) -> None:
    respons = klien_api.get("/aplikasi")

    assert respons.status_code == 200
    assert 'id="form-jadwal"' in respons.text
    assert "Jadwal Rentang Tanggal" in respons.text
    assert 'id="kode-karyawan"' in respons.text
    assert 'id="tanggal-mulai"' in respons.text
    assert 'id="tanggal-selesai"' in respons.text


def test_halaman_memiliki_tombol_ekspor(
    klien_api: TestClient,
) -> None:
    respons = klien_api.get("/aplikasi")

    assert respons.status_code == 200
    assert 'id="ekspor-csv"' in respons.text
    assert 'id="ekspor-excel"' in respons.text