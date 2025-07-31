from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from jose import jwt, JWTError
from sqlalchemy.orm import Session

import config
from database import SessionLocal
from models import User


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request.state.user = None
        token = request.cookies.get("access_token")
        if token:
            try:
                payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
                email = payload.get("sub")
                if email:
                    db: Session = SessionLocal()
                    user = db.query(User).filter(User.email == email).first()
                    db.close()
                    request.state.user = user
            except JWTError:
                pass  # token inválido, no hace nada

        response = await call_next(request)
        return response
