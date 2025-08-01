# models/level.py
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


class Level(Base):
    __tablename__ = "levels"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)  # Ej: "Ritmo y compás"
    description = Column(Text, nullable=True)  # Objetivos del nivel
    order = Column(Integer, unique=True, nullable=False)  # Define secuencia (1, 2, 3...)

    # Visibilidad
    is_published = Column(Boolean, default=True)  # Solo los niveles publicados son accesibles
    is_practice_allowed = Column(Boolean, default=True)  # Pueden repetirlo después

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    activities = relationship("Activity", back_populates="level", cascade="all, delete-orphan")
    responses = relationship("UserActivityResponse", back_populates="level")

    def __str__(self):
        return f"Nivel {self.order}: {self.title}"