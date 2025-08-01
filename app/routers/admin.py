# routers/admin.py
from fastapi import APIRouter, Request, Depends, HTTPException, Response
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from datetime import datetime
from models.user import User
from models.level import Level
from models.activity import Activity
from models.response import UserActivityResponse
from database import get_db
from utils import render_template_with_user, get_current_user

router = APIRouter(prefix="/admin", tags=["admin"])

# === Middleware: solo admin ===
def require_admin(request: Request, db: Session, user):
    if not user or user.role != "admin":
        return RedirectResponse(url="/", status_code=303)
    return None

# === Dashboard principal del admin ===
@router.get("/dashboard", name="admin_dashboard")
async def admin_dashboard(request: Request, db: Session = Depends(get_db), user=Depends(get_current_user)):
    error = require_admin(request, db, user)
    if error:
        return error

    # Todos los usuarios estudiantes
    students = db.query(User).filter(User.role == "student").all()

    # Todos los niveles
    levels = db.query(Level).order_by(Level.order).all()

    # Progreso por alumno
    progress_data = []
    for student in students:
        student_progress = {
            "user": student,
            "current_level": db.query(Level).filter(Level.id == student.current_level_id).first(),
            "completed_levels_count": len(student.completed_levels or []),
            "total_time_spent": 0,
            "latest_activity": None
        }

        # Calcular tiempo total y última actividad
        responses = db.query(UserActivityResponse).filter(UserActivityResponse.user_id == student.id).all()
        for r in responses:
            student_progress["total_time_spent"] += r.time_spent

        latest = db.query(UserActivityResponse).filter(UserActivityResponse.user_id == student.id).order_by(
            UserActivityResponse.created_at.desc()).first()
        student_progress["latest_activity"] = latest

        progress_data.append(student_progress)

    # Ordenar por niveles completados (para ranking)
    progress_data.sort(key=lambda x: x["completed_levels_count"], reverse=True)

    return render_template_with_user(request, "admin/dashboard.html", {
        "students": students,
        "levels": levels,
        "progress_data": progress_data,
        "now": datetime.utcnow()
    }, db=db)

# === Ver informe detallado de un alumno ===
@router.get("/student/{student_id}", name="student_report")
async def student_report(student_id: int, request: Request, db: Session = Depends(get_db), user=Depends(get_current_user)):
    error = require_admin(request, db, user)
    if error:
        return error

    student = db.query(User).filter(User.id == student_id, User.role == "student").first()
    if not student:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")

    # Respuestas del alumno
    responses = db.query(UserActivityResponse).filter(UserActivityResponse.user_id == student_id).order_by(
        UserActivityResponse.level_id, UserActivityResponse.activity_id, UserActivityResponse.attempt_number).all()

    # Agrupar por nivel
    report_by_level = {}
    for r in responses:
        level = db.query(Level).filter(Level.id == r.level_id).first()
        if level.id not in report_by_level:
            report_by_level[level.id] = {
                "level": level,
                "activities": [],
                "total_score": 0,
                "max_score": 0,
                "attempts": 0,
                "time_spent": 0
            }
        report_by_level[level.id]["activities"].append(r)
        report_by_level[level.id]["time_spent"] += r.time_spent
        report_by_level[level.id]["attempts"] += 1

    # Calcular nota final por nivel (último intento)
    final_scores = []
    for level_data in report_by_level.values():
        # Último intento por actividad
        last_responses = {}
        for r in level_data["activities"]:
            key = r.activity_id
            last_responses[key] = r

        total_score = 0
        max_possible = 0
        for r in last_responses.values():
            # Suponemos que "score" es "8/10" → extraemos el numerador
            try:
                score_str = r.score.replace(",", ".")
                if "/" in score_str:
                    score = float(score_str.split("/")[0])
                    max_score = float(score_str.split("/")[1])
                else:
                    score = float(score_str)
                    max_score = 10.0
                total_score += score
                max_possible += max_score
            except:
                continue

        level_data["total_score"] = round(total_score, 2)
        level_data["max_score"] = round(max_possible, 2)
        level_data["final_grade"] = round((total_score / max_possible) * 10 if max_possible > 0 else 0, 2)

        final_scores.append(level_data["final_grade"])

    # Nota media final
    final_average = round(sum(final_scores) / len(final_scores), 2) if final_scores else 0

    return render_template_with_user(request, "admin/student_report.html", {
        "student": student,
        "report_by_level": report_by_level,
        "final_average": final_average
    }, db=db)

# === Ver ranking de progreso (para mostrar a alumnos) ===
@router.get("/leaderboard", name="class_leaderboard")
async def class_leaderboard(request: Request, db: Session = Depends(get_db), user=Depends(get_current_user)):
    error = require_admin(request, db, user)
    if error:
        return error

    students = db.query(User).filter(User.role == "student").all()
    leaderboard = []

    for s in students:
        completed = len(s.completed_levels or [])
        leaderboard.append({
            "full_name": s.full_name,
            "course": s.course,
            "completed_levels": completed,
            "current_level": s.current_level_id
        })

    # Ordenar por niveles completados
    leaderboard.sort(key=lambda x: x["completed_levels"], reverse=True)

    return render_template_with_user(request, "admin/leaderboard.html", {
        "leaderboard": leaderboard
    }, db=db)

# === Exportar datos (opcional, para copiar a boletines) ===
@router.get("/export/grades", name="export_grades")
async def export_grades(request: Request, db: Session = Depends(get_db), user=Depends(get_current_user)):
    error = require_admin(request, db, user)
    if error:
        return error

    students = db.query(User).filter(User.role == "student").all()
    grades_data = []

    for s in students:
        responses = db.query(UserActivityResponse).filter(UserActivityResponse.user_id == s.id).all()
        last_scores = {}
        for r in responses:
            last_scores[r.activity_id] = r  # Sobrescribe → último intento

        total = 0
        max_total = 0
        for r in last_scores.values():
            try:
                if "/" in r.score:
                    score = float(r.score.split("/")[0])
                    max_score = float(r.score.split("/")[1])
                else:
                    score = float(r.score)
                    max_score = 10.0
                total += score
                max_total += max_score
            except:
                continue

        final_grade = round((total / max_total) * 10, 2) if max_total > 0 else 0
        grades_data.append({
            "email": s.email,
            "full_name": s.full_name,
            "course": s.course,
            "final_grade": final_grade,
            "completed_levels": len(s.completed_levels or [])
        })

    # Devolver como texto plano (fácil de copiar a Excel)
    content = "Email,Nombre,Curso,Nota Final,Niveles Completados\n"
    for g in grades_data:
        content += f"{g['email']},{g['full_name']},{g['course']},{g['final_grade']},{g['completed_levels']}\n"

    return Response(
        content=content,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=notas_finales.csv"}
    )