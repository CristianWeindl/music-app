from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from starlette.status import HTTP_303_SEE_OTHER

from models import Quiz
from database import get_db
from utils import render_template_with_user, get_current_user

router = APIRouter()

@router.get("/quizzes", tags=["quizzes"])
async def list_quizzes(request: Request, db: Session = Depends(get_db)):
    return render_template_with_user(request, "quizzes.html", {
        "quizzes": db.query(Quiz).all()
    }, db=db)

@router.get("/quizzes/create", tags=["quizzes"])
async def create_quiz_form(request: Request, db: Session = Depends(get_db)):
    return render_template_with_user(request, "create_quiz.html", {}, db=db)

@router.post("/quizzes/create", tags=["quizzes"])
async def create_quiz(request: Request,
                      title: str = Form(...),
                      description: str = Form(None),
                      db: Session = Depends(get_db),
                      user=Depends(get_current_user)):
    quiz = Quiz(title=title, description=description, owner_id=user.id)
    db.add(quiz)
    db.commit()
    return RedirectResponse("/quizzes", status_code=HTTP_303_SEE_OTHER)

@router.get("/quizzes/edit/{quiz_id}", tags=["quizzes"])
async def edit_quiz_form(request: Request, quiz_id: int, db: Session = Depends(get_db)):
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        return RedirectResponse("/quizzes", status_code=HTTP_303_SEE_OTHER)
    return render_template_with_user(request, "edit_quiz.html", {
        "quiz": quiz
    }, db=db)

@router.post("/quizzes/edit/{quiz_id}", tags=["quizzes"])
async def update_quiz(quiz_id: int,
                      title: str = Form(...),
                      description: str = Form(None),
                      db: Session = Depends(get_db),
                      user=Depends(get_current_user)):
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id, Quiz.owner_id == user.id).first()
    if quiz:
        quiz.title = title
        quiz.description = description
        db.commit()
    return RedirectResponse("/quizzes", status_code=HTTP_303_SEE_OTHER)

@router.get("/quizzes/delete/{quiz_id}", tags=["quizzes"])
async def delete_quiz(quiz_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id, Quiz.owner_id == user.id).first()
    if quiz:
        db.delete(quiz)
        db.commit()
    return RedirectResponse("/quizzes", status_code=HTTP_303_SEE_OTHER)
