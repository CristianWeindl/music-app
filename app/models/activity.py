# models/activity.py
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    level_id = Column(Integer, ForeignKey("levels.id"), nullable=False)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=True)  # Texto descriptivo o enunciado
    media_type = Column(String(20), nullable=True)  # "audio", "video", "image", "none"
    media_url = Column(String(500), nullable=True)  # Enlace a archivo o embed
    activity_type = Column(String(50), nullable=False)  # "multiple_choice", "fill_gaps", "classify_audio"

    # Configuración específica por tipo
    config = Column(JSON, nullable=False)  # Estructura flexible: opciones, correctas, categorías, etc.

    # Control
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    order_in_level = Column(Integer, default=1)  # Orden dentro del nivel
    is_required = Column(Boolean, default=True)  # Si debe completarse para avanzar

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    level = relationship("Level", back_populates="activities")
    owner = relationship("User", back_populates="activities")
    responses = relationship("UserActivityResponse", back_populates="activity")

    def __str__(self):
        return f"[{self.activity_type}] {self.title}"