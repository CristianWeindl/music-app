# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ✅ Importa con ruta absoluta
from app.routers import auth, levels, activities, admin
from app.database import engine, Base
import app.models.user
import app.models.level
import app.models.activity
import app.models.response

# Crear tablas (solo si usas SQLite y no tienes migraciones)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MusicApp Edu",
    description="Plataforma educativa de música para secundaria",
    version="1.0.0"
)

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

@app.get("/")
def home():
    return {"message": "Bienvenido a MusicApp Edu"}