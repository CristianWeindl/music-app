# app/routers/activities.py
from fastapi import APIRouter, Request, Form, Depends, HTTPException, Response
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from starlette.status import HTTP_303_SEE_OTHER
from app.models.activity import Activity
from app.models.level import Level
from app.database import get_db
from app.utils import render_template_with_user, get_current_user

router = APIRouter(prefix="/activities", tags=["activities"])

# === Listar actividades de un nivel ===
@router.get("/level/{level_id}", name="list_activities_by_level")
async def list_activities_by_level(
    request: Request,
    level_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    if not user or user.role != "admin":
        return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)

    level = db.query(Level).filter(Level.id == level_id).first()
    if not level:
        raise HTTPException(status_code=404, detail="Nivel no encontrado")

    activities = db.query(Activity).filter(Activity.level_id == level_id).order_by(Activity.order_in_level).all()
    return render_template_with_user(request, "admin/activities.html", {
        "level": level,
        "activities": activities
    }, db=db)

# === Crear actividad (formulario) ===
@router.get("/create/level/{level_id}", name="create_activity_form")
async def create_activity_form(
    request: Request,
    level_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    if not user or user.role != "admin":
        return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)

    level = db.query(Level).filter(Level.id == level_id).first()
    if not level:
        raise HTTPException(status_code=404, detail="Nivel no encontrado")

    return render_template_with_user(request, "admin/create_activity.html", {
        "level": level
    }, db=db)

# === Crear actividad (POST) ===
@router.post("/create")
async def create_activity(
    request: Request,
    level_id: int = Form(...),
    title: str = Form(...),
    content: str = Form(None),
    media_type: str = Form(None),
    media_url: str = Form(None),
    activity_type: str = Form(...),
    config: str = Form(...),  # JSON string desde el formulario
    order_in_level: int = Form(1),
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    if not user or user.role != "admin":
        return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)

    level = db.query(Level).filter(Level.id == level_id).first()
    if not level:
        raise HTTPException(status_code=404, detail="Nivel no encontrado")

    import json
    try:
        config_data = json.loads(config)
    except json.JSONDecodeError:
        return render_template_with_user(request, "admin/create_activity.html", {
            "level": level,
            "error": "El campo 'config' debe ser un JSON válido."
        }, db=db)

    activity = Activity(
        level_id=level_id,
        title=title,
        content=content,
        media_type=media_type,
        media_url=media_url,
        activity_type=activity_type,
        config=config_data,
        owner_id=user.id,
        order_in_level=order_in_level
    )
    db.add(activity)
    db.commit()
    db.refresh(activity)

    return RedirectResponse(url=f"/activities/level/{level_id}", status_code=HTTP_303_SEE_OTHER)

# === Editar actividad (formulario) ===
@router.get("/edit/{activity_id}", name="edit_activity_form")
async def edit_activity_form(
    request: Request,
    activity_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    if not user or user.role != "admin":
        return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)

    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Actividad no encontrada")

    return render_template_with_user(request, "admin/edit_activity.html", {
        "activity": activity,
        "level": activity.level,
        "config_json": activity.config
    }, db=db)

# === Editar actividad (POST) ===
@router.post("/edit/{activity_id}")
async def update_activity(
    activity_id: int,
    request: Request,
    title: str = Form(...),
    content: str = Form(None),
    media_type: str = Form(None),
    media_url: str = Form(None),
    activity_type: str = Form(...),
    config: str = Form(...),
    order_in_level: int = Form(1),
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    if not user or user.role != "admin":
        return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)

    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Actividad no encontrada")

    import json
    try:
        config_data = json.loads(config)
    except json.JSONDecodeError:
        return render_template_with_user(request, "admin/edit_activity.html", {
            "activity": activity,
            "level": activity.level,
            "error": "El campo 'config' debe ser un JSON válido."
        }, db=db)

    activity.title = title
    activity.content = content
    activity.media_type = media_type
    activity.media_url = media_url
    activity.activity_type = activity_type
    activity.config = config_data
    activity.order_in_level = order_in_level

    db.commit()
    return RedirectResponse(url=f"/activities/level/{activity.level_id}", status_code=HTTP_303_SEE_OTHER)

# === Eliminar actividad ===
@router.get("/delete/{activity_id}")
async def delete_activity(
    activity_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    if not user or user.role != "admin":
        return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)

    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if activity:
        level_id = activity.level_id
        db.delete(activity)
        db.commit()
        return RedirectResponse(url=f"/activities/level/{level_id}", status_code=HTTP_303_SEE_OTHER)

    return RedirectResponse(url="/levels", status_code=HTTP_303_SEE_OTHER)