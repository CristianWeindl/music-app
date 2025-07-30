# Music App

Aplicación web para gestión y práctica musical con autenticación JWT, actividades y cuestionarios.

## Características

- Registro e inicio de sesión con autenticación JWT.
- Gestión de usuarios.
- Actividades interactivas (escucha guiada, cuestionarios).
- Panel de usuario protegido.
- Basado en FastAPI y SQLAlchemy con base de datos SQLite.
- Interfaz con plantillas Jinja2 y estilos CSS.

## Requisitos

- Python 3.8+
- Virtualenv (opcional pero recomendado)

## Instalación

1. Clona el repositorio

```bash
git clone https://github.com/CristianWeindl/music-app.git
cd music-app

2. Crea y activa entorno virtual (opcional pero recomendado)

bash
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

3. Instala dependencias

bash
pip install -r requirements.txt

4. Ejecuta la aplicación

bash
unicorn main:app --reload

5. Abre en navegador

cpp
http://127.0.0.1:8000

Uso básico
Regístrate en /auth/register

Inicia sesión en /auth/login

Accede a actividades protegidas en /activities/quiz y otras rutas

Cierra sesión en /auth/logout

Estructura del proyecto
main.py: Archivo principal para levantar FastAPI

routers/auth.py: Rutas y lógica de autenticación

routers/activities.py: Rutas de actividades

models.py: Definición de modelos de base de datos

database.py: Configuración y sesión de base de datos

templates/: Plantillas HTML

static/: Archivos estáticos (CSS)

config.py: Configuración general

Autor
Cristian Weindl

# music-app
