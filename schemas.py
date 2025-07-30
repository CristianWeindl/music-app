from pydantic import BaseModel
from typing import Optional

# Base común para crear y devolver quizzes
class QuizBase(BaseModel):
    title: str
    description: Optional[str] = None

# Para crear un quiz (POST)
class QuizCreate(QuizBase):
    pass

# Para devolver un quiz (GET)
class Quiz(QuizBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True  # Compatibilidad con SQLAlchemy (Pydantic v2)
