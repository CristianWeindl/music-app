# models/user.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(50), default="student")  # "student", "admin"
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    course = Column(String(10), nullable=True)  # Ej: "1ºA", "3ºB"

    # Progreso
    current_level_id = Column(Integer, nullable=True)  # Último nivel no completado
    completed_levels = Column(JSON, default=list)  # [{level_id, score, time, attempts, completed_at}, ...]

    # Recuperación de contraseña
    reset_token = Column(String(255), nullable=True)
    reset_token_expires = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    activities = relationship("Activity", back_populates="owner")
    responses = relationship("UserActivityResponse", back_populates="user")

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def is_institutional_email(self, allowed_domains):
        """Verifica si el email pertenece a un dominio institucional permitido"""
        if not allowed_domains:
            return True  # Si no hay dominios definidos, permite cualquier correo
        return any(self.email.endswith(f"@{domain.strip()}") for domain in allowed_domains)