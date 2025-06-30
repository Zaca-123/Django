# 🛠️ Django-Relacional

Proyecto académico para UTN Villa María, **Catedra:** Bases de Datos . La aplicación demuestra cómo integrar **Django** con **PostgreSQL** utilizando **Docker** y contenedores.

---

## 📦 Herramientas
![image](https://github.com/user-attachments/assets/d485ae1e-0578-473b-b1d0-ad802a34afae) ![image](https://github.com/user-attachments/assets/b8ea8f51-76de-45df-b77e-c0bb9240e344) ![image](https://github.com/user-attachments/assets/32cdc11d-b8f3-406a-aeea-e0878ed25221) ![image](https://github.com/user-attachments/assets/13483d2b-b516-423c-b29e-7a0c36816823)




- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- Python 3.11 (opcional para desarrollo local sin Docker)
- [Postgres](https://www.postgresql.org/download/)

---

## 🚀 Instalación y ejecución

## 1. Clonar el repositorio:

```bash
git clone https://github.com/Zaca-123/Django-Relacional.git
cd Django-Relacional
````

## 2. Levantar los contenedores
````
docker-compose up --build
````

## 3. Acceder a la aplicación:

````
http://localhost:8000/
````

## 🧪 Migraciones
Para aplicar las migraciones de modelos a la base de datos:

````
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
````
## 👤 Acceso al Admin de Django
Crear superusuario:

````
docker-compose exec web python manage.py createsuperuser
````
## Iniciar sesión:
````
http://localhost:8000/admin/
````
## 📂 Estructura del proyecto
````
Django-Relacional/
├── src/                # Código fuente de Django
├── venv/               # Entorno virtual (opcional)
├── docker-compose.yml  # Configuración de contenedores
├── Dockerfile          # Imagen personalizada de Django
└── requirements.txt    # Dependencias de Python
````

## 📚 Licencia
Este proyecto fue desarrollado como actividad académica y no cuenta con una licencia específica.
