from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.basis_data.koneksi import BasisModel, dapatkan_sesi
from app.basis_data.seed import seed_karyawan
from app.main import aplikasi


@pytest.fixture
def klien_api() -> Generator[TestClient, None, None]:
    """Menyediakan klien API dengan basis data sementara."""

    engine_pengujian = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    BasisModel.metadata.create_all(bind=engine_pengujian)

    sesi_pengujian = sessionmaker(
        bind=engine_pengujian,
        autoflush=False,
        expire_on_commit=False,
    )

    with sesi_pengujian() as sesi:
        seed_karyawan(sesi)

    def timpa_sesi() -> Generator[Session, None, None]:
        with sesi_pengujian() as sesi:
            yield sesi

    aplikasi.dependency_overrides[dapatkan_sesi] = timpa_sesi

    klien = TestClient(aplikasi)

    try:
        yield klien
    finally:
        aplikasi.dependency_overrides.clear()
        BasisModel.metadata.drop_all(bind=engine_pengujian)
        engine_pengujian.dispose()
