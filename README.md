# Sistema de Calificaciones Tributarias - NUAM

Sistema web para la gestión de calificaciones tributarias de instrumentos financieros.

---

## 🛠 Tecnologías

* **Django** 5.x
* **Python** 3.11+
* **PostgreSQL** (Supabase)
* **python-decouple** para manejo de variables de entorno
* **psycopg2-binary** para conexión con PostgreSQL

---

## 🚀 Instalación

Sigue estos pasos para configurar y ejecutar el proyecto localmente:

### 1️⃣ Clonar el repositorio

```bash
git clone git@github.com:DykeByte/NUAM_project.git
cd NUAM_project
```

### 2️⃣ Crear entorno virtual

```bash
python3 -m venv venv
source venv/bin/activate  # macOS / Linux
# venv\Scripts\activate    # Windows
```

### 3️⃣ Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4️⃣ Configurar variables de entorno

1. Copiar el archivo de ejemplo:

```bash
cp .env.example .env
```

2. Rellenar `.env` con tus propias credenciales:

```env
SECRET_KEY=tu_clave_secreta
DEBUG=True
DB_NAME=nombre_base_de_datos
DB_USER=usuario_postgres
DB_PASSWORD=clave_postgres
DB_HOST=host_supabase
DB_PORT=5432
```

> ⚠️ **No compartas tu `.env` con nadie.** Este archivo contiene claves sensibles.

### 5️⃣ Migrar la base de datos

```bash
python manage.py migrate
```

### 6️⃣ Crear superusuario

```bash
python manage.py createsuperuser
```

Sigue las instrucciones para crear un usuario administrador.

### 7️⃣ Ejecutar el servidor

```bash
python manage.py runserver
```

Accede al proyecto en tu navegador:

```
http://127.0.0.1:8000/
```

---

## 📌 Recomendaciones

* Mantén tu `.env` fuera del repositorio (`.gitignore` ya lo protege).
* Para colaborar, tus amigos deben usar **`.env.example`** como plantilla.
* Si trabajas con Supabase, asegúrate de usar los datos de conexión correctos de tu proyecto.

---

## 📂 Estructura del proyecto

* `gestion_tributaria/` → app principal para manejar la gestión de calificaciones.
* `sistema_tributario/` → configuración del proyecto Django.
* `.env.example` → ejemplo de variables de entorno.
* `requirements.txt` → dependencias del proyecto.
* `manage.py` → script de administración de Django.

---

## 👥 Colaboración

1. Clonar el repo.
2. Copiar `.env.example` a `.env` y rellenar variables con credenciales propias.
3. Instalar dependencias (`pip install -r requirements.txt`).
4. Migrar base de datos (`python manage.py migrate`).
5. Ejecutar servidor (`python manage.py runserver`).


