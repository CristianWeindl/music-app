# app/routers/admin.py
from fastapi import APIRouter, Request, Depends, HTTPException, Response
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from datetime import datetime
from app.models.user import User
from app.models.level import Level
from app.models.activity import Activity
from app.models.response import UserActivityResponse
from app.database import get_db
from app.utils import render_template_with_user, get_current_user

# ... (resto del archivo igual)