# 🐍 Django + BBDD (PostgreSQL → MongoDB)

Repositorio profe: [fabrica_pastas](https://github.com/pindutn/fabrica_pastas/tree/main)

Este proyecto te guía para levantar una app Django usando Docker, conectarla inicialmente a PostgreSQL y luego migrar todo a MongoDB usando `djongo`.

---

## 🚀 Puesta en marcha (con PostgreSQL)

### 1. Generar los proyectos y levantar el backend

```bash
docker compose run --rm generate
sudo chown $USER:$USER -R .
docker compose up -d backend
```

### 2. Migrar la base de datos

```bash
docker compose run --rm manage makemigrations
docker compose run --rm manage migrate
```

### 3. Crear un superusuario

```bash
docker compose run --rm manage createsuperuser
```

### 4. Cargar datos iniciales

```bash
docker compose run --rm manage loaddata initial_data
```

👉 Ahora podés ingresar a [http://localhost:8000/admin](http://localhost:8000/admin) y loguearte con el usuario creado para administrar los objetos.

---

## 🔄 Migración a MongoDB

### 1. Agregar MongoDB en el `docker-compose.yml`

```yaml
mongo:
  image: mongo:latest
  container_name: mongo
  environment:
    - MONGO_INITDB_ROOT_USERNAME=mongo
    - MONGO_INITDB_ROOT_PASSWORD=mongo
    - MONGO_INITDB_DATABASE=mongo
  volumes:
    - mongo-data:/data/db
  ports:
    - "27017:27017"
  networks:
    - net

volumes:
  mongo-data:
```

### 2. Modificar el `models.py`

Reemplazá la importación de `models` por:

```python
from djongo import models
```

### 3. Cambiar la configuración de la base de datos en `settings.py`

```python
DATABASES = {
    "default": {
        "ENGINE": "djongo",
        "NAME": "mongo",
        "CLIENT": {
            "host": "mongo",
            "port": 27017,
            "username": "mongo",
            "password": "mongo",
            "authSource": "admin",  # Importante para autenticación
        },
    },
    "old_db": {
        "ENGINE": DATABASE_ENGINE,
        "NAME": POSTGRES_DB,
        "USER": POSTGRES_USER,
        "PASSWORD": POSTGRES_PASSWORD,
        "HOST": POSTGRES_HOST,
        "PORT": POSTGRES_PORT,
    },
}
```

### 4. Limpiar migraciones anteriores

Eliminá todos los archivos dentro de `app/migrations/`, excepto el `__init__.py`.

### 5. Reconstruir la imagen Docker

```bash
docker compose build
```

### 6. Levantar servicios con MongoDB

```bash
docker compose up -d
```

### 7. Migrar modelos a MongoDB

```bash
docker compose run manage makemigrations
docker compose run manage migrate
```

### 8. Crear nuevamente el superusuario

```bash
docker compose run --rm manage createsuperuser
```

### 9. Ejecutar el comando personalizado de migración

```bash
docker compose run --rm manage migrate_to_mongo
```

✅ ¡Listo! Ahora los datos fueron migrados exitosamente a **MongoDB**.  
Podés corroborarlo accediendo nuevamente a [http://localhost:8000/admin](http://localhost:8000/admin) con las credenciales del paso anterior.
