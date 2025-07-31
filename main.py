from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from routers import auth, activities, quizzes
from database import Base, engine, get_db
from utils import render_template_with_user

app = FastAPI()

# Crear tablas
Base.metadata.create_all(bind=engine)

# Montar archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Incluir routers
app.include_router(auth.router)
app.include_router(activities.router)
app.include_router(quizzes.router)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request, db=Depends(get_db)):
    return render_template_with_user(request, "base.html", {}, db=db)

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, db=Depends(get_db)):
    return render_template_with_user(request, "dashboard.html", {}, db=db)
