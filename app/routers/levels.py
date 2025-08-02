# routers/levels.py
from fastapi import APIRouter, Request, Form, Depends, HTTPException, Response
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from starlette.status import HTTP_303_SEE_OTHER
from app.models.level import Level
from app.models.activity import Activity
from app.database import get_db
from utils import render_template_with_user, get_current_user

router = APIRouter(prefix="/levels", tags=["levels"])

# === Listar niveles (solo admin) ===
@router.get("/", name="list_levels")
async def list_levels(request: Request, db: Session = Depends(get_db), user=Depends(get_current_user)):
    if not user or user.role != "admin":
        return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)

    levels = db.query(Level).order_by(Level.order).all()
    return render_template_with_user(request, "admin/levels.html", {
        "levels": levels
    }, db=db)

# === Crear nivel (formulario) ===
@router.get("/create", name="create_level_form")
async def create_level_form(request: Request, db: Session = Depends(get_db), user=Depends(get_current_user)):
    if not user or user.role != "admin":
        return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
    return render_template_with_user(request, "admin/create_level.html", {}, db=db)

# === Crear nivel (POST) ===
@router.post("/create")
async def create_level(
    request: Request,
    title: str = Form(...),
    description: str = Form(None),
    order: int = Form(...),
    is_published: bool = Form(False),
    is_practice_allowed: bool = Form(True),
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    if not user or user.role != "admin":
        return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)

    # Verificar que el orden no esté duplicado
    existing = db.query(Level).filter(Level.order == order).first()
    if existing:
        return render_template_with_user(request, "admin/create_level.html", {
            "error": f"Ya existe un nivel con orden {order}. Elige otro.",
            "title": title,
            "description": description,
            "order": order,
            "is_published": is_published,
            "is_practice_allowed": is_practice_allowed
        }, db=db)

    level = Level(
        title=title,
        description=description,
        order=order,
        is_published=is_published,
        is_practice_allowed=is_practice_allowed
    )
    db.add(level)
    db.commit()
    db.refresh(level)

    return RedirectResponse(url="/levels", status_code=HTTP_303_SEE_OTHER)

# === Editar nivel (formulario) ===
@router.get("/edit/{level_id}", name="edit_level_form")
async def edit_level_form(request: Request, level_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    if not user or user.role != "admin":
        return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)

    level = db.query(Level).filter(Level.id == level_id).first()
    if not level:
        raise HTTPException(status_code=404, detail="Nivel no encontrado")

    return render_template_with_user(request, "admin/edit_level.html", {
        "level": level
    }, db=db)

# === Editar nivel (POST) ===
@router.post("/edit/{level_id}")
async def update_level(
    level_id: int,
    request: Request,
    title: str = Form(...),
    description: str = Form(None),
    order: int = Form(...),
    is_published: bool = Form(False),
    is_practice_allowed: bool = Form(True),
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    if not user or user.role != "admin":
        return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)

    level = db.query(Level).filter(Level.id == level_id).first()
    if not level:
        raise HTTPException(status_code=404, detail="Nivel no encontrado")

    # Si cambia el orden, verificar que no esté duplicado
    if level.order != order:
        existing = db.query(Level).filter(Level.order == order).first()
        if existing:
            return render_template_with_user(request, "admin/edit_level.html", {
                "level": level,
                "error": f"Ya existe un nivel con orden {order}. Elige otro."
            }, db=db)

    level.title = title
    level.description = description
    level.order = order
    level.is_published = is_published
    level.is_practice_allowed = is_practice_allowed

    db.commit()
    return RedirectResponse(url="/levels", status_code=HTTP_303_SEE_OTHER)

# === Eliminar nivel ===
@router.get("/delete/{level_id}")
async def delete_level(level_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    if not user or user.role != "admin":
        return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)

    level = db.query(Level).filter(Level.id == level_id).first()
    if level:
        db.delete(level)
        db.commit()

    return RedirectResponse(url="/levels", status_code=HTTP_303_SEE_OTHER)