# routers/auth.py
from fastapi import APIRouter, Request, Form, Depends, Response, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from passlib.hash import bcrypt
from datetime import datetime, timedelta
from models.user import User
from database import get_db
from utils import render_template_with_user, create_access_token, get_current_user, generate_reset_token, send_password_reset_email
import config

router = APIRouter(prefix="/auth", tags=["auth"])

@router.get("/register", name="register_form")
async def register_form(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if user:
        return RedirectResponse(url="/dashboard", status_code=302)
    return render_template_with_user(request, "auth/register.html", {}, db=db)

@router.post("/register")
async def register(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    first_name: str = Form(...),
    last_name: str = Form(...),
    course: str = Form(None),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == email).first()
    if user:
        return render_template_with_user(request, "auth/register.html", {"error": "Este correo ya está registrado."}, db=db)

    # Validar dominio institucional
    if not User(email=email, first_name=first_name, last_name=last_name).is_institutional_email(config.ALLOWED_INSTITUTIONAL_DOMAINS):
        return render_template_with_user(request, "auth/register.html", {
            "error": f"Debes usar un correo de dominio autorizado: {', '.join(config.ALLOWED_INSTITUTIONAL_DOMAINS)}"
        }, db=db)

    hashed_password = bcrypt.hash(password)
    new_user = User(
        email=email,
        hashed_password=hashed_password,
        first_name=first_name,
        last_name=last_name,
        course=course,
        role="student"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return RedirectResponse(url="/auth/login", status_code=302)

@router.get("/login", name="login_form")
async def login_form(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if user:
        return RedirectResponse(url="/dashboard", status_code=302)
    return render_template_with_user(request, "auth/login.html", {}, db=db)

@router.post("/login")
async def login(
    request: Request,
    response: Response,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == email).first()
    if not user or not bcrypt.verify(password, user.hashed_password):
        return render_template_with_user(request, "auth/login.html", {"error": "Credenciales inválidas"}, db=db)

    token_data = {"sub": user.email}
    token = create_access_token(data=token_data)
    response = RedirectResponse(url="/dashboard", status_code=302)
    response.set_cookie(key="access_token", value=token, httponly=True, max_age=86400)
    return response

@router.get("/logout")
async def logout():
    response = RedirectResponse(url="/")
    response.delete_cookie("access_token")
    return response

@router.get("/forgot-password", name="forgot_password_form")
async def forgot_password_form(request: Request, db: Session = Depends(get_db)):
    return render_template_with_user(request, "auth/forgot_password.html", {}, db=db)

@router.post("/forgot-password")
async def forgot_password(
    request: Request,
    email: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return render_template_with_user(request, "auth/forgot_password.html", {
            "message": "Si el correo existe, recibirás un enlace para recuperar tu contraseña."
        }, db=db)

    # Generar token
    token = generate_reset_token()
    user.reset_token = token
    user.reset_token_expires = datetime.utcnow() + timedelta(hours=1)
    db.commit()

    # Enviar correo
    send_password_reset_email(email, token)

    return render_template_with_user(request, "auth/forgot_password.html", {
        "message": "Si el correo existe, recibirás un enlace para recuperar tu contraseña."
    }, db=db)

@router.get("/reset-password", name="reset_password_form")
async def reset_password_form(request: Request, token: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.reset_token == token).first()
    if not user or not user.reset_token_expires or user.reset_token_expires < datetime.utcnow():
        return render_template_with_user(request, "auth/forgot_password.html", {
            "error": "El enlace de recuperación es inválido o ha expirado."
        }, db=db)
    return render_template_with_user(request, "auth/reset_password.html", {"token": token}, db=db)

@router.post("/reset-password")
async def reset_password(
    request: Request,
    token: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.reset_token == token).first()
    if not user or not user.reset_token_expires or user.reset_token_expires < datetime.utcnow():
        return render_template_with_user(request, "auth/forgot_password.html", {
            "error": "El enlace de recuperación es inválido o ha expirado."
        }, db=db)

    user.hashed_password = bcrypt.hash(password)
    user.reset_token = None
    user.reset_token_expires = None
    db.commit()

    return RedirectResponse(url="/auth/login", status_code=302)