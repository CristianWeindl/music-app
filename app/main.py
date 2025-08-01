# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, levels, activities, admin
from database import engine, Base
import models.user
import models.level
import models.activity
import models.response

# Crear tablas en la base de datos (solo si usas SQLite y no tienes migraciones)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MusicApp Edu",
    description="Plataforma educativa de música para secundaria",
    version="1.0.0"
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambia esto en producción
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
    return {
        "message": "Bienvenido a MusicApp Edu",
        "docs": "/docs",
        "redoc": "/redoc"
    }