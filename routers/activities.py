from fastapi import APIRouter, Depends
from routers.auth import get_current_user

router = APIRouter(prefix="/activities", tags=["activities"])

@router.get("/listen")
def listen_activity():
    return {"message": "Actividad de escucha guiada"}

@router.get("/quiz")
def quiz_activity(user=Depends(get_current_user)):
    return {"message": f"Bienvenido al cuestionario, {user.email}."}
