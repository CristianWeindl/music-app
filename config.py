# config.py
import os
from datetime import timedelta

# === Configuración general ===
SECRET_KEY = os.getenv("SECRET_KEY", "tu_clave_secreta_muy_segura_cambia_esto")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 24

# === Dominios institucionales permitidos ===
# Puedes cambiar esto cada año escolar
ALLOWED_INSTITUTIONAL_DOMAINS = [
    "instituto-escolar.es",
    "colegio2025.es",
    "academiamusical.edu"
]

# === Configuración de correo (SMTP) para recuperación de contraseña ===
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USERNAME = os.getenv("SMTP_USERNAME", "tuemail@gmail.com")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "tu_app_password_aqui")
EMAIL_FROM = os.getenv("EMAIL_FROM", "notificaciones@musiceduapp.com")

# === URL base de la app (para enlaces en correos) ===
BASE_URL = os.getenv("BASE_URL", "https://tu-music-app.onrender.com")