# Tutorial: Despliegue de una Aplicación Django con Docker
Práctico de Mapeo Objeto-Relacional para la materia, Bases de Datos de la carrera `Ingeniería en Sistemas` de la *`Universidad Tecnológica Nacional`* *`Facultad Regional Villa María`*.

![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Django 5.1.11](https://img.shields.io/badge/Django%205.1.11-092E20?style=for-the-badge&logo=django&logoColor=white)
![Alpine Linux](https://img.shields.io/badge/Alpine_Linux-0D597F?style=for-the-badge&logo=alpine-linux&logoColor=white)
![Python 3.13](https://img.shields.io/badge/Python%203.13-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PostgreSQL 17](https://img.shields.io/badge/PostgreSQL%2017-336791?style=for-the-badge&logo=postgresql&logoColor=white)

**Referencia Rápida**

**Mantenido Por:** Grupo 12

## **Descargo de Responsabilidad:**
El código proporcionado se ofrece "tal cual", sin garantía de ningún tipo, expresa o implícita. En ningún caso los autores o titulares de derechos de autor serán responsables de cualquier reclamo, daño u otra responsabilidad.

## Introducción
Este tutorial te guiará paso a paso en la creación y despliegue de una aplicación Django utilizando Docker y Docker Compose. El objetivo es que puedas levantar un entorno de desarrollo profesional, portable y fácil de mantener, ideal tanto para pruebas como para producción.

---

## Requisitos Previos
- **Docker** y **Docker Compose** instalados en tu sistema. Puedes consultar la [documentación oficial de Docker](https://docs.docker.com/get-docker/) para la instalación.
- Conocimientos básicos de Python y Django (no excluyente, el tutorial es autoexplicativo).

### Recursos Útiles
- [Tutorial oficial de Django](https://docs.djangoproject.com/en/2.0/intro/tutorial01/)
- [Cómo crear un entorno virtual en Python](https://docs.djangoproject.com/en/2.0/intro/contributing/)

---

## 1. Clonar el Repositorio
Clona este repositorio y navega al directorio del proyecto.

> **Puedes copiar todo este bloque y pegarlo directamente en tu terminal.**
```bash
git clone https://github.com/Zaca-123/Django-Relacional.git
cd Django-Relacional
```

---

## 2. Estructura del Proyecto
El proyecto cuenta con la siguiente estructura:

```
Django-Relacional/
├── docker-compose.yml
├── Dockerfile
├── LICENSE
├── README.md
├── requirements.txt
└── src/
    ├── manage.py
    ├── app/
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── models.py
    │   ├── tests.py
    │   ├── views.py
    │   ├── fixtures/
    │   │   └── initial_data.json
    │   └── migrations/
    │       ├── __init__.py
    │       └── 0001_initial.py
    └── VentaEntrada/
        ├── __init__.py
        ├── asgi.py
        ├── settings.py
        ├── urls.py
        └── wsgi.py
```

---

## 3. Archivos de Configuración

### Dependencias - `requirements.txt`
El archivo ya incluye las dependencias necesarias para el proyecto:

```txt
Django
psycopg[binary]  # Driver para PostgreSQL
```

### Dockerfile
La imagen de Docker está configurada para crear un entorno optimizado con Alpine Linux y Python 3.13.

### Docker Compose - `docker-compose.yml`
Orquesta los servicios necesarios: base de datos PostgreSQL y la aplicación Django.

---

## 4. 🚀 Instalación y Ejecución

### Levantar los contenedores
> **Puedes copiar todo este bloque y pegarlo directamente en tu terminal.**
```bash
docker-compose up --build
```

### Acceder a la aplicación
```
http://localhost:8000/
```

---

## 5. 🧪 Configuración Inicial

### Aplicar migraciones
Para aplicar las migraciones de modelos a la base de datos:

> **Puedes copiar todo este bloque y pegarlo directamente en tu terminal.**
```bash
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```

### Crear superusuario
> **Puedes copiar todo este bloque y pegarlo directamente en tu terminal.**
```bash
docker-compose exec web python manage.py createsuperuser
```

### Cargar datos iniciales
> **Puedes copiar todo este bloque y pegarlo directamente en tu terminal.**
```bash
docker-compose exec web python manage.py loaddata initial_data
```

---

## 6. 👤 Acceso al Admin de Django
Iniciar sesión en el panel de administración:
```
http://localhost:8000/admin/
```

---

## 7. Comandos Útiles

### Ver logs de los contenedores
> **Puedes copiar todo este bloque y pegarlo directamente en tu terminal.**
```bash
docker-compose logs -f
```

### Detener y eliminar contenedores
> **Puedes copiar todo este bloque y pegarlo directamente en tu terminal.**
```bash
docker-compose down
```

### Detener y eliminar contenedores con imágenes y contenedores sin uso
> **Puedes copiar todo este bloque y pegarlo directamente en tu terminal.**
```bash
docker-compose down -v --remove-orphans --rmi all
```

### Limpiar recursos de Docker
> **Puedes copiar todo este bloque y pegarlo directamente en tu terminal.**
```bash
docker system prune -a
```

### Ejecutar comandos de Django
> **Puedes copiar todo este bloque y pegarlo directamente en tu terminal.**
```bash
# Crear nuevas migraciones
docker-compose exec web python manage.py makemigrations

# Aplicar migraciones
docker-compose exec web python manage.py migrate

# Acceder al shell de Django
docker-compose exec web python manage.py shell

# Recopilar archivos estáticos
docker-compose exec web python manage.py collectstatic
```

---

## 8. Modelado de la Aplicación

### Modelos Implementados
La aplicación `app` incluye los siguientes modelos:

- **Localidad, Barrio, Provincia**: Modelos geográficos
- **Producto**: Productos con cálculo automático de precios
- **Cliente**: Información completa de clientes
- **Venta y DetalleVenta**: Sistema de ventas con detalles
- **Ingrediente, UnidadMedida, Receta**: Sistema de recetas para productos

### Administración
El panel de administración de Django está configurado con:
- Interfaz optimizada para gestión de productos con recetas inline
- Gestión de ventas con detalles inline
- Filtros y búsquedas avanzadas
- Ordenamiento y paginación

---

## 9. Funcionalidades Principales

- **Gestión de Productos**: Con sistema de recetas e ingredientes
- **Cálculo Automático de Precios**: Basado en costos de ingredientes y ganancia
- **Gestión de Clientes**: Con información completa y ubicación
- **Sistema de Ventas**: Con detalles y seguimiento
- **Panel de Administración**: Interfaz completa para gestión

---

## 10. Desarrollo y Contribución

### Estructura de la Base de Datos
El proyecto utiliza PostgreSQL con las siguientes características:
- Relaciones bien definidas entre modelos
- Índices optimizados para consultas frecuentes
- Validaciones a nivel de modelo y base de datos

### Personalización
Puedes extender el proyecto agregando:
- Nuevos modelos en `src/app/models.py`
- Configuraciones de admin en `src/app/admin.py`
- Vistas personalizadas en `src/app/views.py`
- Datos iniciales en `src/app/fixtures/`

---

## 🤝 Créditos y Licencia

- **Mantenido por:** Grupo 12
- **Institución:** Universidad Tecnológica Nacional - Facultad Regional Villa María
- **Materia:** Bases de Datos - Ingeniería en Sistemas
- **Basado en el repositorio:** [fábrica de pastas](https://github.com/pindutn/fabrica_pastas/tree/main)

> El código se entrega "tal cual", sin garantías. Si te es útil, considera dar feedback.

---

## Conclusión
Con este proyecto tienes un entorno Django profesional, portable y listo para desarrollo o producción. Recuerda consultar la documentación oficial de Django y Docker para profundizar en cada tema. ¡Éxitos en tu proyecto!

---
