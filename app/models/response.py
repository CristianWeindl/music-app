# models/response.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


class UserActivityResponse(Base):
    __tablename__ = "user_responses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    activity_id = Column(Integer, ForeignKey("activities.id"), nullable=False)
    level_id = Column(Integer, ForeignKey("levels.id"), nullable=False)

    response_data = Column(JSON, nullable=False)  # Lo que respondió el alumno
    is_correct = Column(Boolean, nullable=False)
    score = Column(String(10), nullable=False)  # "8/10", "Correcto", etc.
    time_spent = Column(Integer, default=0)  # segundos
    attempt_number = Column(Integer, default=1)  # 1º, 2º intento...

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relaciones
    user = relationship("User", back_populates="responses")
    activity = relationship("Activity", back_populates="responses")
    level = relationship("Level", back_populates="responses")

    def __str__(self):
        return f"{self.user.email} → {self.activity.title} (Intento {self.attempt_number})"