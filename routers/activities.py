from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from starlette.status import HTTP_303_SEE_OTHER

from models import Activity
from database import get_db
from utils import render_template_with_user, get_current_user

router = APIRouter()

@router.get("/activities", tags=["activities"])
async def list_activities(request: Request, db: Session = Depends(get_db)):
    return render_template_with_user(request, "activities.html", {
        "activities": db.query(Activity).all()
    }, db=db)

@router.get("/activities/create", tags=["activities"])
async def create_activity_form(request: Request, db: Session = Depends(get_db)):
    return render_template_with_user(request, "create_activity.html", {}, db=db)

@router.post("/activities/create", tags=["activities"])
async def create_activity(request: Request,
                          title: str = Form(...),
                          description: str = Form(None),
                          db: Session = Depends(get_db),
                          user=Depends(get_current_user)):
    activity = Activity(title=title, description=description, owner_id=user.id)
    db.add(activity)
    db.commit()
    return RedirectResponse("/activities", status_code=HTTP_303_SEE_OTHER)

@router.get("/activities/edit/{activity_id}", tags=["activities"])
async def edit_activity_form(request: Request, activity_id: int, db: Session = Depends(get_db)):
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        return RedirectResponse("/activities", status_code=HTTP_303_SEE_OTHER)
    return render_template_with_user(request, "edit_activity.html", {
        "activity": activity
    }, db=db)

@router.post("/activities/edit/{activity_id}", tags=["activities"])
async def update_activity(activity_id: int,
                          title: str = Form(...),
                          description: str = Form(None),
                          db: Session = Depends(get_db),
                          user=Depends(get_current_user)):
    activity = db.query(Activity).filter(Activity.id == activity_id, Activity.owner_id == user.id).first()
    if activity:
        activity.title = title
        activity.description = description
        db.commit()
    return RedirectResponse("/activities", status_code=HTTP_303_SEE_OTHER)

@router.get("/activities/delete/{activity_id}", tags=["activities"])
async def delete_activity(activity_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    activity = db.query(Activity).filter(Activity.id == activity_id, Activity.owner_id == user.id).first()
    if activity:
        db.delete(activity)
        db.commit()
    return RedirectResponse("/activities", status_code=HTTP_303_SEE_OTHER)
