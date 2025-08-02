# app/main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.routers import auth, levels, activities, admin
from app.database import engine, Base
import app.models.user
import app.models.level
import app.models.activity
import app.models.response
from app.utils import set_templates

# Crear tablas
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MusicApp Edu",
    description="Plataforma educativa de música para secundaria",
    version="1.0.0"
)

# Montar archivos estáticos
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Configurar plantillas
templates = Jinja2Templates(directory="app/templates")
set_templates(templates)  # Inyectar en utils.py

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(auth.router)
app.include_router(levels.router)
app.include_router(activities.router)
app.include_router(admin.router)

# === Ruta principal: redirige a login o dashboard ===
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})