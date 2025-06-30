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
