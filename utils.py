from fastapi import Request, Depends, HTTPException, status, Cookie
from fastapi.templating import Jinja2Templates
from jose import JWTError, jwt
from sqlalchemy.orm import Session

import config
from models import User
from database import get_db

templates = Jinja2Templates(directory="templates")

def render_template_with_user(request: Request, template_name: str, context: dict = {}, db: Session = None):
    token = request.cookies.get("access_token")
    user = None

    if token:
        try:
            payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
            email = payload.get("sub")
            if email and db:
                user = db.query(User).filter(User.email == email).first()
        except JWTError:
            pass

    context.update({"request": request, "user": user})
    return templates.TemplateResponse(template_name, context)

# ✅ CAMBIADO: usar token desde cookie
def get_current_user(access_token: str = Cookie(None), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if not access_token:
        raise credentials_exception

    try:
        payload = jwt.decode(access_token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    return user
