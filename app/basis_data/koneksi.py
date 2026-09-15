from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.inti.konfigurasi import konfigurasi


class BasisModel(DeclarativeBase):
    """Kelas dasar untuk seluruh model SQLAlchemy."""


engine = create_engine(
    konfigurasi.url_basis_data,
    connect_args={"check_same_thread": False},
)

SesiLokal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)


def dapatkan_sesi() -> Generator[Session, None, None]:
    """Menyediakan sesi basis data untuk dependency FastAPI."""

    sesi = SesiLokal()

    try:
        yield sesi
    finally:
        sesi.close()
