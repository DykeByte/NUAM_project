# Sistema de Calificaciones Tributarias - NUAM

Sistema web para la gestión de calificaciones tributarias de instrumentos financieros.

## Instalación

1. Clonar el repositorio
2. Crear entorno virtual: `python3 -m venv venv`
3. Activar: `source venv/bin/activate`
4. Instalar dependencias: `pip install -r requirements.txt`
5. Configurar .env
6. Migrar: `python manage.py migrate`
7. Crear superusuario: `python manage.py createsuperuser`

## Tecnologías

- Django 5.x
- PostgreSQL (Supabase)
- Python 3.11+

