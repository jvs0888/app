from pathlib import Path
from fastapi import Request, APIRouter, Depends, HTTPException
from fastapi.responses import Response, HTMLResponse, RedirectResponse
from fastapi_limiter.depends import RateLimiter

try:
    from app.templates import templates
    from app.auth import auth
except ImportError as ie:
    exit(f'{ie} :: {Path(__file__).resolve()}')


index = APIRouter()


@index.get(path='/', response_class=HTMLResponse, dependencies=[Depends(RateLimiter(times=5, seconds=10))])
async def index_page(request: Request, is_access: dict = Depends(auth.validate_token)):
    if is_access:
        return RedirectResponse(url='/dashboard')
    return templates.TemplateResponse('index/index.html', {'request': request})
