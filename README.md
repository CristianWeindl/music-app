# 🎵 MusicApp Edu

Plataforma educativa de música para secundaria, diseñada para profesores que quieren evaluar de forma continua y gamificada.

Los alumnos avanzan por **niveles**, completan actividades multimedia y practican sin presión.  
Tú, como profesor, ves su progreso, notas y tiempo invertido, y generas la **nota teórica final** para el boletín.

---

## 🌟 Características principales

- ✅ **Autenticación con correo institucional**
- ✅ **Progreso por niveles** (no actividades sueltas)
- ✅ **Actividades multimedia**: audio, video, imágenes
- ✅ **Tipos de ejercicios**:
  - Test (opción única)
  - Completar huecos con clic
  - Clasificación de obras por características
- ✅ **Evaluación continua**: se guarda tiempo, intentos y evolución
- ✅ **Nota final calculada** (último intento prevalece)
- ✅ **Gamificación**: ranking por niveles completados (no por notas)
- ✅ **Panel de administrador**:
  - Ver progreso por alumno
  - Exportar notas a CSV
  - Gestionar niveles y actividades
- ✅ **Recuperación de contraseña por email**

---

## 🛠 Tecnología utilizada

- **FastAPI** – Backend
- **SQLAlchemy** – ORM
- **PostgreSQL** – Base de datos (en Render)
- **Jinja2** – Plantillas HTML
- **Bootstrap 5** – Diseño responsive
- **Render.com** – Despliegue

---

## 🚀 Despliegue en Render

1. Crea una cuenta en [Render.com](https://render.com)
2. Conecta tu repositorio de GitHub
3. Render detectará automáticamente `render.yaml`
4. El servicio y la base de datos se crearán automáticamente
5. Tu app estará disponible en `https://music-app-edu.onrender.com`

> 🔐 Asegúrate de configurar:
> - `SMTP_USERNAME` y `SMTP_PASSWORD` (usa una App Password de Gmail)
> - `ALLOWED_INSTITUTIONAL_DOMAINS` (dominios permitidos para registro)

---

## 🧪 Credenciales de prueba

### Profesor (admin)
- **Email**: `profesor@instituto-escolar.es`
- **Contraseña**: `123456`

### Alumno de ejemplo
- **Email**: `alumno@instituto-escolar.es`
- **Contraseña**: `123456`
- **Nombre**: Juan Pérez
- **Curso**: 1ºA

> ⚠️ Cambia estas contraseñas en producción.

---

## 📂 Estructura del proyecto
