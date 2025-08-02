# app/config.py
import os

SECRET_KEY = os.getenv("SECRET_KEY", "tu_clave_secreta_muy_larga_y_segura")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 24

# Dominios institucionales permitidos
ALLOWED_INSTITUTIONAL_DOMAINS = os.getenv(
    "ALLOWED_INSTITUTIONAL_DOMAINS",
    "instituto-escolar.es,colegio2025.es,academiamusical.edu"
).split(",")

# Configuración SMTP para recuperación de contraseña
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")  # Tu correo
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")  # App Password
EMAIL_FROM = os.getenv("EMAIL_FROM", "notificaciones@musiceduapp.com")

# URL base de la app (para enlaces en correos)
BASE_URL = os.getenv("BASE_URL", "https://music-app-edu.onrender.com")