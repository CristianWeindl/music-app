# app/utils.py
from fastapi import Request
from jose import jwt
from datetime import datetime, timedelta
import random
import string
from passlib.hash import bcrypt
from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_HOURS, SMTP_SERVER, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD, EMAIL_FROM, BASE_URL
from app.database import get_db
from app.models.user import User

# Variable global para templates (inyectada desde main.py)
templates = None

def set_templates(t):
    global templates
    templates = t

# === JWT y autenticación ===
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except:
        return None

# === Obtener usuario actual desde cookie ===
def get_current_user(request: Request, db):
    token = request.cookies.get("access_token")
    if not token:
        return None
    payload = decode_access_token(token)
    if not payload or not payload.get("sub"):
        return None
    email = payload.get("sub")
    user = db.query(User).filter(User.email == email).first()
    return user

# === Renderizar plantillas con usuario ===
def render_template_with_user(request: Request, template_name: str, context: dict, db=None):
    user = None
    if db:
        user = get_current_user(request, db)
    if "user" not in context:
        context["user"] = user
    if templates is None:
        raise Exception("Templates no inicializados. Llama a set_templates() en main.py")
    return templates.TemplateResponse(template_name, {"request": request, **context})

# === Generar token de recuperación ===
def generate_reset_token():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=32))

# === Enviar correo de recuperación ===
def send_password_reset_email(email: str, token: str):
    try:
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
    except ImportError as e:
        print(f"Error al importar email.mime: {e}")
        return False

    msg = MIMEMultipart()
    msg['From'] = EMAIL_FROM
    msg['To'] = email
    msg['Subject'] = "Recupera tu contraseña en MusicApp Edu"

    reset_link = f"{BASE_URL}/auth/reset-password?token={token}"

    body = f"""
    Hola,

    Has solicitado recuperar tu contraseña. Haz clic en el siguiente enlace para crear una nueva:

    {reset_link}

    Si no solicitaste este cambio, ignora este correo.

    Saludos,
    El equipo de MusicApp Edu
    """
    msg.attach(MIMEText(body, 'plain'))

    try:
        import smtplib
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(EMAIL_FROM, email, msg.as_string())
        server.close()
        return True
    except Exception as e:
        print(f"Error al enviar correo: {e}")
        return False