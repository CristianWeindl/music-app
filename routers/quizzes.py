from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import Quiz, User
from schemas import QuizCreate, Quiz
from routers.auth import get_current_user

router = APIRouter(prefix="/quizzes", tags=["quizzes"])

@router.post("/", response_model=Quiz)
def create_quiz(
    quiz: QuizCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_quiz = Quiz(**quiz.dict(), owner_id=current_user.id)
    db.add(db_quiz)
    db.commit()
    db.refresh(db_quiz)
    return db_quiz

@router.get("/", response_model=List[Quiz])
def get_quizzes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    quizzes = db.query(Quiz).filter(Quiz.owner_id == current_user.id).all()
    return quizzes
