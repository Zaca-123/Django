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

## 3. Definición de Dependencias
El archivo `requirements.txt` ya incluye las dependencias necesarias para tu aplicación:

> **Este es el contenido actual del archivo requirements.txt en el proyecto:**
```txt
Django==3.2.24
djongo==1.3.6
sqlparse==0.2.4
pymongo==3.12.3
psycopg2-binary==2.9.9
```

---

## 4. Creación del Dockerfile Existente
El `Dockerfile` actual define la imagen de Docker que contiene tu aplicación. Utiliza Python 3.12 Alpine y está optimizado para el proyecto de venta de entradas.

> **Este es el Dockerfile actual del proyecto:**
```dockerfile
FROM python:3.12-alpine AS base
LABEL maintainer="Grupo 12 <grupo12@gmail.com>"
LABEL version="1.0"
LABEL description="cloudset"

RUN apk --no-cache add bash pango ttf-freefont py3-pip curl

FROM base AS builder
RUN apk --no-cache add \
    libpq-dev gcc musl-dev python3-dev postgresql-dev \
    py3-pillow py3-brotli py3-scipy py3-cffi \
    linux-headers autoconf automake libtool cmake \
    fortify-headers binutils libffi-dev wget openssl-dev libc-dev \
    g++ make musl-dev pkgconf libpng-dev openblas-dev build-base \
    font-noto terminus-font libffi

WORKDIR /install
COPY ./requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

FROM base
RUN mkdir /code
WORKDIR /code
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY . /code
RUN ln -s /usr/share/zoneinfo/America/Cordoba /etc/localtime

CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "app.wsgi"]
```

---

## 5. Configuración de Variables de Entorno Existente
El archivo `.env.db` ya está configurado con las variables de entorno necesarias para la conexión a la base de datos:

> **Este es el contenido actual del archivo .env.db:**
```conf
DATABASE_ENGINE=django.db.backends.postgresql_psycopg2
POSTGRES_DB=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_USER=postgres
PGUSER=${POSTGRES_USER}
POSTGRES_PASSWORD=postgres
LANG=es_AR.utf8
POSTGRES_INITDB_ARGS="--locale-provider=icu --icu-locale=es-AR --auth-local=trust"
```

---

## 6. Definición de Servicios con Docker Compose Existente
El archivo `docker-compose.yml` actual orquesta los servicios necesarios para el sistema de venta de entradas:

> **Este es el docker-compose.yml actual del proyecto:**
```yml
services:
  db:
    image: postgres:alpine
    env_file:
      - .env.db
    environment:
      - POSTGRES_INITDB_ARGS=--auth-host=md5 --auth-local=trust
    healthcheck:
      test: ["CMD-SHELL", "pg_isready"]
      interval: 10s
      timeout: 2s
      retries: 5
    volumes:
      - postgres-db:/var/lib/postgresql/data
    networks:
      - net
    ports:
      - "6666:5432"

  backend:
    build: .
    command: runserver 0.0.0.0:8000
    entrypoint: python3 manage.py
    env_file:
      - .env.db
    expose:
      - "8000"
    ports:
      - "8000:8000"
    volumes:
      - ./src:/code
    depends_on:
      db:
        condition: service_healthy
    networks:
      - net

  generate:
    build: .
    user: root
    command: /bin/sh -c 'mkdir src && django-admin startproject app src'
    env_file:
      - .env.db
    depends_on:
      db:
        condition: service_healthy
    volumes:
      - .:/code
    networks:
      - net

  manage:
    build: .
    entrypoint: python3 manage.py
    env_file:
      - .env.db
    volumes:
      - ./src:/code
    depends_on:
      db:
        condition: service_healthy
    networks:
      - net

networks:
  net:

volumes:
  postgres-db:
```

**Nota Importante:** El servicio principal se llama `backend` en este proyecto, no `web`.

---

## 7. Configuración y Ejecución del Proyecto Existente

### El proyecto ya está configurado, para ejecutarlo sigue estos pasos:

> **Puedes copiar todo este bloque y pegarlo directamente en tu terminal.**
```bash
# 1. Construir e iniciar todos los servicios
docker-compose up --build

# 2. En otra terminal, aplicar migraciones
docker-compose exec backend python manage.py makemigrations
docker-compose exec backend python manage.py migrate

# 3. Crear superusuario
docker-compose exec backend python manage.py createsuperuser

# 4. Cargar datos iniciales
docker-compose exec backend python manage.py loaddata initial_data
```

### Acceder a la aplicación
```
http://localhost:8000/
```

**Panel de Administración:**
```
http://localhost:8000/admin/
```

**Base de Datos PostgreSQL (puerto externo):**
```
Host: localhost
Puerto: 6666
Usuario: postgres
Contraseña: postgres
Base de Datos: postgres
```

---

## 8. Modelado Actual de la Aplicación

### Sistema de Venta de Entradas
El proyecto implementa un sistema completo para la venta de entradas a eventos con los siguientes modelos:

> **Este es el archivo ./src/app/models.py actual:**
```python
from django.db import models

class TipoDNI(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    nro_dni = models.IntegerField()
    tipo_dni = models.ForeignKey(TipoDNI, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class MedioDePago(models.Model):
    descripcion = models.CharField(max_length=100)

    def __str__(self):
        return self.descripcion

class Evento(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha = models.DateField()
    hora = models.TimeField()
    capacidad = models.IntegerField()

    def __str__(self):
        return self.nombre

class Entrada(models.Model):
    descripcion = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)

    def __str__(self):
        return self.descripcion

class Venta(models.Model):
    fecha = models.DateField()
    hora = models.TimeField()
    importe = models.DecimalField(max_digits=10, decimal_places=2)
    medio_de_pago = models.ForeignKey(MedioDePago, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

    def __str__(self):
        return f"Venta {self.id} - {self.fecha}"

class DetalleDeVenta(models.Model):
    descripcion = models.CharField(max_length=100)
    cant_entradas = models.IntegerField()
    importe_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    entrada = models.ForeignKey(Entrada, on_delete=models.CASCADE)

    def __str__(self):
        return self.descripcion
```

---

## 9. Administración Actual de la Aplicación

### Configuración del Admin Django
El panel de administración ya está configurado para gestionar todos los modelos:

> **Este es el archivo ./src/app/admin.py actual:**
```python
from django.contrib import admin
from .models import *

admin.site.register(Cliente)
admin.site.register(TipoDNI)
admin.site.register(MedioDePago)
admin.site.register(Evento)
admin.site.register(Entrada)
admin.site.register(Venta)
admin.site.register(DetalleDeVenta)
```

### Mejoras Sugeridas para el Admin
> **Puedes reemplazar el contenido de ./src/app/admin.py con esta versión mejorada:**
```python
from django.contrib import admin
from .models import *

@admin.register(TipoDNI)
class TipoDNIAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ['nombre']

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'nro_dni', 'tipo_dni')
    search_fields = ['nombre', 'apellido', 'nro_dni']
    list_filter = ('tipo_dni',)
    ordering = ['apellido', 'nombre']

@admin.register(MedioDePago)
class MedioDePagoAdmin(admin.ModelAdmin):
    list_display = ('descripcion',)
    search_fields = ['descripcion']

@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha', 'hora', 'capacidad')
    search_fields = ['nombre', 'descripcion']
    list_filter = ('fecha',)
    date_hierarchy = 'fecha'
    ordering = ['-fecha', 'hora']

@admin.register(Entrada)
class EntradaAdmin(admin.ModelAdmin):
    list_display = ('descripcion', 'evento', 'precio')
    search_fields = ['descripcion', 'evento__nombre']
    list_filter = ('evento',)
    ordering = ['evento', 'precio']

class DetalleDeVentaInline(admin.TabularInline):
    model = DetalleDeVenta
    extra = 0
    fields = ('entrada', 'cant_entradas', 'importe_unitario', 'descripcion')
    readonly_fields = ('importe_unitario',)

@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ('id', 'fecha', 'hora', 'cliente', 'importe', 'medio_de_pago')
    search_fields = ['cliente__nombre', 'cliente__apellido']
    list_filter = ('fecha', 'medio_de_pago')
    date_hierarchy = 'fecha'
    ordering = ['-fecha', '-hora']
    inlines = [DetalleDeVentaInline]

@admin.register(DetalleDeVenta)
class DetalleDeVentaAdmin(admin.ModelAdmin):
    list_display = ('venta', 'entrada', 'cant_entradas', 'importe_unitario')
    search_fields = ['venta__id', 'entrada__descripcion']
    list_filter = ('entrada__evento',)
```

---

## 10. Datos Iniciales del Sistema

### Fixtures Existentes
El proyecto ya incluye datos de ejemplo para comenzar a trabajar:

> **Ejemplo del contenido de ./src/app/fixtures/initial_data.json:**
```json
[
  {
    "model": "app.TipoDNI",
    "pk": 1,
    "fields": {
      "nombre": "DNI"
    }
  },
  {
    "model": "app.TipoDNI",
    "pk": 2,
    "fields": {
      "nombre": "Pasaporte"
    }
  },
  {
    "model": "app.Cliente",
    "pk": 1,
    "fields": {
      "nombre": "Juan",
      "apellido": "Pérez",
      "nro_dni": 12345678,
      "tipo_dni": 1
    }
  },
  // ... más datos de clientes, eventos, entradas, etc.
]
```

### Cargar los Datos Iniciales
> **Puedes copiar este comando para cargar los datos:**
```bash
docker-compose exec backend python manage.py loaddata initial_data
```

---

## 11. Comandos Útiles para el Proyecto

### Trabajar con el proyecto usando Docker Compose
**Importante:** En este proyecto el servicio principal se llama `backend`, no `web`.

> **Comandos principales para desarrollo:**
```bash
# Iniciar todos los servicios
docker-compose up -d

# Ver logs en tiempo real
docker-compose logs -f

# Ver logs solo del backend
docker-compose logs -f backend

# Ver logs solo de la base de datos
docker-compose logs -f db

# Detener todos los servicios
docker-compose down

# Detener y eliminar volúmenes (CUIDADO: elimina la base de datos)
docker-compose down -v

# Reconstruir las imágenes y reiniciar
docker-compose up --build

# Acceder al shell del contenedor backend
docker-compose exec backend bash

# Acceder al shell de Django
docker-compose exec backend python manage.py shell

# Crear migraciones
docker-compose exec backend python manage.py makemigrations

# Aplicar migraciones
docker-compose exec backend python manage.py migrate

# Crear superusuario
docker-compose exec backend python manage.py createsuperuser

# Cargar datos iniciales
docker-compose exec backend python manage.py loaddata initial_data

# Ver estado de los contenedores
docker-compose ps

# Reiniciar un servicio específico
docker-compose restart backend
docker-compose restart db
```

### Comandos de limpieza y mantenimiento
> **Comandos para limpiar el entorno:**
```bash
# Limpiar contenedores, redes e imágenes no utilizadas
docker system prune -f

# Limpiar solo contenedores detenidos
docker container prune -f

# Limpiar solo imágenes no utilizadas
docker image prune -f

# Limpiar solo volúmenes no utilizados
docker volume prune -f

# Reiniciar completamente el proyecto
docker-compose down -v --remove-orphans
docker system prune -f
docker-compose up --build
```

### Comandos específicos de Django
> **Comandos para administrar la aplicación Django:**
```bash
# Verificar la configuración del proyecto
docker-compose exec backend python manage.py check

# Ver todas las migraciones disponibles
docker-compose exec backend python manage.py showmigrations

# Ver el SQL de una migración específica
docker-compose exec backend python manage.py sqlmigrate app 0001

# Revertir migraciones (CUIDADO)
docker-compose exec backend python manage.py migrate app zero

# Ejecutar tests
docker-compose exec backend python manage.py test

# Recopilar archivos estáticos
docker-compose exec backend python manage.py collectstatic

# Ver la versión de Django
docker-compose exec backend python manage.py version

# Abrir el shell de la base de datos
docker-compose exec backend python manage.py dbshell

# Crear un dump de la base de datos
docker-compose exec db pg_dump -U postgres postgres > backup.sql

# Restaurar un dump de la base de datos
docker-compose exec db psql -U postgres postgres < backup.sql
```

---

## 12. Funcionalidades del Sistema de Venta de Entradas

### Gestión de Eventos
- **Eventos Completos**: Nombre, descripción, fecha, hora y capacidad
- **Control de Capacidad**: Limitación de entradas por evento
- **Programación**: Gestión de fechas y horarios

### Gestión de Entradas
- **Tipos de Entrada**: Diferentes categorías por evento
- **Precios Diferenciados**: Cada tipo de entrada tiene su precio
- **Asociación a Eventos**: Las entradas están vinculadas a eventos específicos

### Gestión de Clientes
- **Datos Personales**: Nombre, apellido y documentos
- **Tipos de Documento**: DNI, Pasaporte, etc.
- **Trazabilidad**: Historial de compras por cliente

### Sistema de Ventas
- **Registro de Ventas**: Fecha, hora e importe total
- **Medios de Pago**: Efectivo, tarjeta, transferencia, etc.
- **Detalles de Venta**: Cantidad de entradas y precios por tipo
- **Control de Stock**: Seguimiento de entradas vendidas vs. capacidad

### Panel de Administración
- **Interfaz Optimizada**: Formularios inline para gestión eficiente
- **Filtros por Fecha**: Navegación por períodos
- **Búsquedas Avanzadas**: Por cliente, evento, fecha
- **Reportes**: Listados organizados por fecha y cliente

---

## 13. Estructura de la Base de Datos del Sistema

### Modelos Principales
- **TipoDNI**: Tipos de documentos (DNI, Pasaporte)
- **Cliente**: Información completa de clientes
- **MedioDePago**: Formas de pago disponibles
- **Evento**: Eventos con programación y capacidad
- **Entrada**: Tipos de entradas por evento con precios
- **Venta**: Transacciones de venta
- **DetalleDeVenta**: Detalles de cada venta con cantidades

### Relaciones del Sistema
- **Cliente → TipoDNI**: Cada cliente tiene un tipo de documento
- **Entrada → Evento**: Las entradas pertenecen a eventos específicos
- **Venta → Cliente**: Cada venta está asociada a un cliente
- **Venta → MedioDePago**: Cada venta tiene un medio de pago
- **DetalleDeVenta → Venta**: Los detalles pertenecen a una venta
- **DetalleDeVenta → Entrada**: Cada detalle especifica el tipo de entrada

### Características del Modelo
- **Integridad Referencial**: CASCADE para mantener consistencia
- **Campos Obligatorios**: Validaciones a nivel de modelo
- **Representación String**: Métodos `__str__` para interfaz amigable
- **Escalabilidad**: Diseño preparado para crecimiento

---


## 14. Solución de Problemas Comunes

### Problemas de Conexión a la Base de Datos
```bash
# Verificar estado de los contenedores
docker-compose ps

# Ver logs de la base de datos
docker-compose logs db

# Ver logs del backend
docker-compose logs backend

# Reiniciar servicios
docker-compose restart db
docker-compose restart backend

# Verificar conectividad desde el backend
docker-compose exec backend ping db
```

### Problemas con Migraciones
```bash
# Ver estado actual de las migraciones
docker-compose exec backend python manage.py showmigrations

# Ver migraciones pendientes
docker-compose exec backend python manage.py showmigrations --plan

# Aplicar migraciones específicas
docker-compose exec backend python manage.py migrate app 0001

# Ver SQL de una migración sin aplicarla
docker-compose exec backend python manage.py sqlmigrate app 0001

# Marcar una migración como aplicada (sin ejecutarla)
docker-compose exec backend python manage.py migrate app 0001 --fake

# Revertir todas las migraciones de una app
docker-compose exec backend python manage.py migrate app zero
```

### Problemas de Permisos (Linux/Mac)
```bash
# Cambiar propietario de archivos
sudo chown -R $USER:$USER .

# Dar permisos de escritura
chmod -R 755 src/

# Ver permisos actuales
ls -la
```

### Problemas con el Puerto 8000
```bash
# Ver qué proceso está usando el puerto 8000
netstat -tulpn | grep :8000

# En Windows:
netstat -ano | findstr :8000

# Matar el proceso que está usando el puerto
sudo kill -9 <PID>

# En Windows:
taskkill /PID <PID> /F

# Cambiar el puerto en docker-compose.yml
# Modificar la línea: "8001:8000" en lugar de "8000:8000"
```

### Limpiar y Reconstruir el Proyecto
```bash
# Parar todos los contenedores
docker-compose down

# Limpiar volúmenes (CUIDADO: elimina la base de datos)
docker-compose down -v

# Limpiar imágenes del proyecto
docker-compose down --rmi all

# Limpiar todo el sistema Docker
docker system prune -a -f

# Reconstruir desde cero
docker-compose build --no-cache
docker-compose up -d

# Restaurar la base de datos
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py loaddata initial_data
```

### Problemas con las Dependencias
```bash
# Reconstruir la imagen Python
docker-compose build --no-cache backend

# Ver las dependencias instaladas
docker-compose exec backend pip list

# Instalar dependencia faltante
docker-compose exec backend pip install <paquete>

# Actualizar requirements.txt con nuevas dependencias
docker-compose exec backend pip freeze > requirements.txt
```

### Problemas de Memoria o Performance
```bash
# Ver uso de recursos
docker stats

# Limitar memoria del contenedor (en docker-compose.yml)
# Agregar bajo el servicio backend:
# deploy:
#   resources:
#     limits:
#       memory: 512M

# Ver logs de errores específicos
docker-compose logs --tail=50 backend | grep ERROR
```

### Backup y Restauración de la Base de Datos
```bash
# Crear backup de la base de datos
docker-compose exec db pg_dump -U postgres -d postgres > backup_$(date +%Y%m%d_%H%M%S).sql

# Restaurar desde backup
docker-compose exec -T db psql -U postgres -d postgres < backup_20241201_120000.sql

# Backup con compresión
docker-compose exec db pg_dump -U postgres -d postgres | gzip > backup_$(date +%Y%m%d_%H%M%S).sql.gz

# Restaurar backup comprimido
gunzip -c backup_20241201_120000.sql.gz | docker-compose exec -T db psql -U postgres -d postgres
```

---

## 🤝 Créditos y Licencia

- **Mantenido por:** Grupo 12
- **Institución:** Universidad Tecnológica Nacional - Facultad Regional Villa María
- **Materia:** Bases de Datos - Ingeniería en Sistemas
- **Basado en el repositorio:** [fábrica de pastas](https://github.com/pindutn/fabrica_pastas/tree/main)

> El código se entrega "tal cual", sin garantías. Si te es útil, considera dar feedback.

---

## Conclusión
Con este proyecto tienes un entorno Django profesional, portable y listo para desarrollo o producción. Recuerda consultar la documentación oficial de Django y Docker para profundizar en cada tema.

---
