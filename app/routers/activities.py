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

    activities = db.query(Activity).filter(Activity.level_id == level_id).order_by(Activity.order_in