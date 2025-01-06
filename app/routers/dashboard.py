from pathlib import Path
from fastapi import Request, APIRouter, Depends
from fastapi.responses import HTMLResponse, RedirectResponse

try:
    from app.templates import templates
    from app.auth import auth
except ImportError as ie:
    exit(f'{ie} :: {Path(__file__).resolve()}')


dashboard = APIRouter()


@dashboard.get(path='/dashboard', response_class=HTMLResponse)
async def dashboard_page(request: Request, is_access: dict = Depends(auth.validate_token)):
    if not is_access:
        return RedirectResponse(url='/login')
    return templates.TemplateResponse('dashboard/dashboard.html', {'request': request})
