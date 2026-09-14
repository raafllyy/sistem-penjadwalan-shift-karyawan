from pydantic_settings import BaseSettings, SettingsConfigDict


class Konfigurasi(BaseSettings):
    """Konfigurasi utama aplikasi."""

    nama_aplikasi: str = "Sistem Penjadwalan Shift Karyawan"
    versi_aplikasi: str = "1.0.0"
    mode_debug: bool = True
    url_basis_data: str = "sqlite:///./database.sqlite3"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


konfigurasi = Konfigurasi()