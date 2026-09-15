from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


def daftarkan_penanganan_error(aplikasi: FastAPI) -> None:
    """Mendaftarkan seluruh penanganan error aplikasi."""

    @aplikasi.exception_handler(HTTPException)
    async def tangani_http_exception(
        _: Request,
        exception: HTTPException,
    ) -> JSONResponse:
        """Menangani HTTPException dengan format respons yang konsisten."""

        return JSONResponse(
            status_code=exception.status_code,
            content={
                "berhasil": False,
                "pesan": str(exception.detail),
            },
        )

    @aplikasi.exception_handler(RequestValidationError)
    async def tangani_validasi_request(
        _: Request,
        __: RequestValidationError,
    ) -> JSONResponse:
        """Menangani kesalahan validasi parameter permintaan."""

        return JSONResponse(
            status_code=422,
            content={
                "berhasil": False,
                "pesan": "Parameter permintaan tidak valid.",
            },
        )
