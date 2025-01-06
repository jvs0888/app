from pathlib import Path
from fastapi import Request, APIRouter, HTTPException, Depends, status
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from authlib.integrations.starlette_client import OAuthError

try:
    from settings.config import config
    from app.templates import templates
    from app.models import UserForm
    from app.auth import auth, oauth
    from database.database import db
    from database.models import UserSchema
except ImportError as ie:
    exit(f'{ie} :: {Path(__file__).resolve()}')


login = APIRouter()


@login.get(path='/login', response_class=HTMLResponse)
async def login_page(request: Request, is_access: dict = Depends(auth.validate_token)):
    if is_access:
        return RedirectResponse(url='/dashboard')
    return templates.TemplateResponse('login/login.html', {'request': request})


@login.post(path='/sign-in', response_class=Response)
async def sign_in(user: UserForm, response: Response):
    db_user: UserSchema = await db.get_user(email=user.email)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    if not auth.verify_password(password=user.password, hashed_password=db_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    token: str = auth.sign_jwt(user_id=db_user.id)
    response.set_cookie(value=token, **config.COOKIE)
    response.status_code = status.HTTP_200_OK
    return response


@login.post(path='/sign-up', response_class=Response)
async def sign_up(user: UserForm, request: Request, response: Response):
    if await db.get_user(email=user.email):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)

    hashed_password: str = auth.hash_password(password=user.password)
    user_id: int = await db.add_user(email=user.email, password=hashed_password)

    token: str = auth.sign_jwt(user_id=user_id)
    response.set_cookie(value=token, **config.COOKIE)
    response.status_code = status.HTTP_201_CREATED
    return response


@login.get('/auth/google', response_class=RedirectResponse)
async def google_login(request: Request):
    redirect_uri: str = request.url_for('google_callback')
    return await oauth.google.authorize_redirect(request=request, redirect_uri=redirect_uri)


@login.get('/auth/google/callback', response_class=RedirectResponse)
async def google_callback(request: Request):
    try:
        token: dict = await oauth.google.authorize_access_token(request=request)
    except OAuthError:
        return RedirectResponse(url='/login')

    email: str = token['userinfo']['email']
    user: UserSchema = await db.get_user(email=email)
    user_id: int = user.id if user else await db.add_user(email=email)

    response: RedirectResponse = RedirectResponse(url='/dashboard')
    token: str = auth.sign_jwt(user_id=user_id)
    response.set_cookie(value=token, **config.COOKIE)
    return response
