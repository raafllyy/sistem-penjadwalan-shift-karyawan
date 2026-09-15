from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(
    include_in_schema=False,
)

template = Jinja2Templates(
    directory="app/template",
)


@router.get(
    "/aplikasi",
    response_class=HTMLResponse,
)
def halaman_utama(request: Request) -> HTMLResponse:
    """Menampilkan halaman utama sistem."""

    return template.TemplateResponse(
        request=request,
        name="index.html",
    )
