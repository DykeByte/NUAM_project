# Sistema de Calificaciones Tributarias - NUAM

Web app para gestionar calificaciones tributarias de instrumentos financieros.

## Instalación rápida

1. Clonar el repositorio:

```bash
git clone https://github.com/DykeByte/NUAM_project.git
cd django_nuam_app
Crear y activar entorno virtual:

bash
Copiar código
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
Instalar dependencias:

bash
Copiar código
pip install -r requirements.txt
Configurar .env con tus credenciales (incluyendo PostgreSQL en Railway).

Aplicar migraciones:

bash
Copiar código
python manage.py migrate
Crear superusuario para acceder al admin:

bash
Copiar código
python manage.py createsuperuser
Ejecutar servidor local:

bash
Copiar código
python manage.py runserver
Modelos principales
Perfil → Roles y datos de usuario.

CargaMasiva → Registro de cargas de datos.

CalificacionTributaria → Información y factores tributarios.

LogOperacion → Historial de operaciones y cargas.

Base de datos
PostgreSQL en Railway

Tablas creadas automáticamente desde las migraciones (0001_initial.py).

Notas
No subir tu .env con credenciales reales.

Usar .env.example como guía para otros desarrolladores.
