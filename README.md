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
Crea un archivo `requirements.txt` para listar las dependencias de Python necesarias para tu aplicación.

> **Puedes copiar todo este bloque y pegarlo directamente en tu archivo requirements.txt.**
```txt
Django
psycopg[binary]  # Driver para PostgreSQL
```

---

## 4. Creación del Dockerfile
El `Dockerfile` define la imagen de Docker que contendrá tu aplicación. Aquí se detallan las etapas de construcción, instalación de dependencias y configuración del entorno.

> **Puedes copiar todo este bloque y pegarlo directamente en tu archivo Dockerfile.**
```dockerfile
# Etapa de construcción
FROM python:3.13-alpine AS base
LABEL maintainer="Grupo 12 <grupo12@utn.edu.ar>"
LABEL version="1.0"
LABEL description="Django-Relacional"
RUN apk --no-cache add bash pango ttf-freefont py3-pip curl

# Etapa de construcción
FROM base AS builder
# Instalación de dependencias de construcción
RUN apk --no-cache add py3-pip py3-pillow py3-brotli py3-scipy py3-cffi \
  linux-headers autoconf automake libtool gcc cmake python3-dev \
  fortify-headers binutils libffi-dev wget openssl-dev libc-dev \
  g++ make musl-dev pkgconf libpng-dev openblas-dev build-base \
  font-noto terminus-font libffi

# Copia solo los archivos necesarios para instalar dependencias de Python
COPY ./requirements.txt .

# Instalación de dependencias de Python
RUN pip install --upgrade pip \
  && pip install --no-cache-dir -r requirements.txt \
  && rm requirements.txt

# Etapa de producción
FROM base
RUN mkdir /code
WORKDIR /code
# Copia solo los archivos necesarios desde la etapa de construcción
COPY ./requirements.txt .
RUN pip install -r requirements.txt \
  && rm requirements.txt
COPY --chown=user:group --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages 
ENV PATH /usr/local/lib/python3.13/site-packages:$PATH
# Configuración adicional
RUN ln -s /usr/share/zoneinfo/America/Cordoba /etc/localtime

# Comando predeterminado
CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "VentaEntrada.wsgi"]
```

---

## 5. Configuración de Variables de Entorno
Crea un archivo `.env.db` para almacenar las variables de entorno necesarias para la conexión a la base de datos.

> **Puedes copiar todo este bloque y pegarlo directamente en tu archivo .env.db.**
```conf
# .env.db
DATABASE_ENGINE=django.db.backends.postgresql
POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_DB=postgres
POSTGRES_USER=postgres
PGUSER=${POSTGRES_USER}
POSTGRES_PASSWORD=postgres
LANG=es_AR.utf8
POSTGRES_INITDB_ARGS="--locale-provider=icu --icu-locale=es-AR --auth-local=trust"
```

---

## 6. Definición de Servicios con Docker Compose
El archivo `docker-compose.yml` orquesta los servicios necesarios: base de datos, backend de Django y utilidades para generación y administración del proyecto.

> **Puedes copiar todo este bloque y pegarlo directamente en tu archivo docker-compose.yml.**
```yml
services:
  db:
    image: postgres:alpine
    env_file:
      - .env.db
    environment:
      - POSTGRES_INITDB_ARGS=--auth-host=md5 --auth-local=trust
    healthcheck:
      test: [ "CMD-SHELL", "pg_isready" ]
      interval: 10s
      timeout: 2s
      retries: 5
    volumes:
      - postgres-db:/var/lib/postgresql/data
    networks:
      - net

  web:
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
    command: /bin/sh -c 'mkdir src && django-admin startproject VentaEntrada src'
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

---

## 7. Generación y Configuración de la Aplicación

### Generar la estructura base del proyecto y la app

Hay que tener el archivo `LICENSE` para que la generación de la imagen no produzca un error.
> **Puedes copiar todo este bloque y pegarlo directamente en tu terminal.**
```bash
# Crear archivo LICENSE vacío
touch LICENSE

# Generar estructura del proyecto Django
docker-compose run --rm generate

# Crear la aplicación 'app'
docker-compose run --rm manage startapp app

# Cambiar permisos de archivos (Linux/Mac)
# En Windows no es necesario este comando
sudo chown $USER:$USER -R .
```

### Configuración de `settings.py`
Edita el archivo `settings.py` para agregar tu app y configurar la base de datos usando las variables de entorno.

> **Puedes copiar todo este bloque y pegarlo al final directamente en tu archivo ./src/VentaEntrada/settings.py.**
```python
import os

ALLOWED_HOSTS = [os.environ.get("ALLOWED_HOSTS", "*")]

INSTALLED_APPS += [
    'app',  # Agrega tu app aquí
]

# Configuración de la base de datos
DATABASE_ENGINE = os.environ.get("DATABASE_ENGINE", "")
POSTGRES_USER = os.getenv("POSTGRES_USER", "")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "")
POSTGRES_DB = os.environ.get("POSTGRES_DB", "") or os.getenv("DB_NAME")
POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "") or os.getenv("DB_HOST")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT", "") or os.getenv("DB_PORT")

DATABASES = {
    "default": {
        "ENGINE": DATABASE_ENGINE,
        "NAME": POSTGRES_DB,
        "USER": POSTGRES_USER,
        "PASSWORD": POSTGRES_PASSWORD,
        "HOST": POSTGRES_HOST,
        "PORT": POSTGRES_PORT,
    }
}

# Configuración de idioma y zona horaria
LANGUAGE_CODE = 'es-ar'
TIME_ZONE = 'America/Argentina/Cordoba'
USE_I18N = True
USE_TZ = True
```

---

## 8. Primeros Pasos con Django

### Migrar la base de datos
> **Puedes copiar todo este bloque y pegarlo directamente en tu terminal.**
```bash
docker-compose run --rm manage migrate
```

### Crear un superusuario
> **Puedes copiar todo este bloque y pegarlo directamente en tu terminal.**
```bash
docker-compose run --rm manage createsuperuser
```

### Iniciar la aplicación
> **Puedes copiar todo este bloque y pegarlo directamente en tu terminal.**
```bash
docker-compose up -d web
```
Accede a la administración de Django en [http://localhost:8000/admin/](http://localhost:8000/admin/)

### Ver logs de los contenedores
> **Puedes copiar todo este bloque y pegarlo directamente en tu terminal.**
```bash
docker-compose logs -f
```

---

## 9. Modelado de la Aplicación

### Ejemplo de `models.py`
Incluye modelos bien documentados y estructurados para una gestión profesional de tus datos.

> **Puedes copiar todo este bloque y pegarlo directamente en tu archivo ./src/app/models.py.**
```python
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


class NombreAbstract(models.Model):
    nombre = models.CharField(
        _('Nombre'),
        help_text=_('Nombre descriptivo'),
        max_length=200,
        # unique=True,
    )

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.upper()
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.nombre}'

    class Meta:
        abstract = True
        ordering = ['nombre']


class Localidad(NombreAbstract):
    class Meta:
        verbose_name = 'localidad'
        verbose_name_plural = 'localidades'


class Barrio(NombreAbstract):
    class Meta:
        verbose_name = 'barrio'
        verbose_name_plural = 'barrios'


class Provincia(NombreAbstract):
    class Meta:
        verbose_name = 'provincia'
        verbose_name_plural = 'provincias'


class Producto(NombreAbstract):
    ganancia = models.DecimalField(
        _('Ganancia'),
        max_digits=15,
        decimal_places=2,
        help_text=_('Ganancia del producto, expresado en coeficiente.'),
        default=0
    )
    es_relleno = models.BooleanField(
        _('Es Relleno'),
        help_text=_('Especifica si el producto contiene relleno.'),
        default=False
    )

    @property
    def precio(self):
        total = 0
        for ingrediente in self.ingredientes.all():
            total += ingrediente.cantidad * ingrediente.ingrediente.costo
        return round(total * self.ganancia, 2)

    class Meta:
        verbose_name = 'producto'
        verbose_name_plural = 'productos'


class Cliente(NombreAbstract):
    numero_documento = models.BigIntegerField(
        _('numero documento'),
        help_text=_('numero de documento / CUIT'),
        null=True
    )
    direccion = models.CharField(
        _('dirección'),
        help_text=_('dirección del cliente'),
        max_length=200,
        blank=True,
        null=True
    )
    celular = models.BigIntegerField(
        _('Celular'),
        help_text=_(
            'Número de celular con característica del/la administrador/a'),
        blank=True,
        null=True
    )
    telefono = models.BigIntegerField(
        _('teléfono'),
        help_text=_('teléfono fijo'),
        blank=True,
        null=True
    )
    email = models.EmailField(
        _('email'),
        help_text=_('email del cliente'),
        null=True,
        blank=True,
    )
    barrio = models.ForeignKey(
        Barrio,
        verbose_name=_('barrio'),
        help_text=_('barrio donde reside '),
        related_name='%(app_label)s_%(class)s_related',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    localidad = models.ForeignKey(
        Localidad,
        verbose_name=_('localidad'),
        help_text=_('localidad donde reside el cliente'),
        related_name='%(app_label)s_%(class)s_related',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    provincia = models.ForeignKey(
        Provincia,
        verbose_name=_('provincia'),
        help_text=_('provincia donde reside'),
        related_name='%(app_label)s_%(class)s_related',
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )
    user = models.ForeignKey(
        User,
        help_text=_('Usuario con el que se loguea al sistema'),
        verbose_name='usuario',
        related_name='%(app_label)s_%(class)s',
        related_query_name='%(app_label)s_%(class)s',
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )

    def __str__(self):
        return '{} {}'.format(self.nombre, self.numero_documento)

    class Meta:
        indexes = [
            models.Index(
                fields=[
                    'numero_documento',
                    'user',
                ],
                name='%(app_label)s_%(class)s_unico'
            ),
        ]


class Venta(models.Model):
    fecha = models.DateField(
        _('fecha'),
        help_text=_('fecha de la venta')
    )
    cliente = models.ForeignKey(
        Cliente,
        verbose_name=_('cliente'),
        help_text=_('cliente que realiza la compra'),
        related_name='compras',
        on_delete=models.PROTECT,
        blank=False,
        null=False
    )

    def __str__(self):
        return '{} {}'.format(self.fecha, self.cliente.nombre)

    class Meta:
        ordering = ['fecha']
        verbose_name = 'venta'
        verbose_name_plural = 'ventas'


class DetalleVenta(models.Model):
    venta = models.ForeignKey(
        Venta,
        verbose_name=_('venta'),
        help_text=_('detalle de la compra'),
        related_name='detalle',
        on_delete=models.PROTECT,
        blank=False,
        null=False
    )
    cantidad = models.DecimalField(
        _('cantidad'),
        max_digits=15,
        decimal_places=2,
        help_text=_('cantidad'),
        blank=True,
        null=True,
        default=None
    )
    producto = models.ForeignKey(
        Producto,
        verbose_name=_('producto'),
        help_text=_('producto'),
        related_name='detalle',
        on_delete=models.PROTECT,
        blank=False,
        null=False
    )


class UnidadMedida(NombreAbstract):
    class Meta:
        verbose_name = 'unidad de medida'
        verbose_name_plural = 'unidades de medida'


class Ingrediente(NombreAbstract):
    costo = models.DecimalField(
        _('Costo'),
        max_digits=15,
        decimal_places=2,
        help_text=_('Costo del ingrediente expresado en pesos'),
        default=0
    )
    unidad_medida = models.ForeignKey(
        UnidadMedida,
        related_name='ingredientes',
        on_delete=models.PROTECT,
        help_text=_('Unidad de medida del ingrediente'),
        null=False,
        blank=False,
        default=1
    )

    class Meta:
        verbose_name = _('Ingrediente')
        verbose_name_plural = _('Ingredientes')


class Receta(models.Model):
    cantidad = models.DecimalField(
        _('Cantidad'),
        max_digits=15,
        decimal_places=3,
        help_text=_(
            'Cantidad del ingrediente, expresado en su unidad de medida.'),
        default=0
    )
    ingrediente = models.ForeignKey(
        Ingrediente,
        related_name='productos',
        on_delete=models.PROTECT,
        help_text=_('Ingrediente de la receta'),
    )
    producto = models.ForeignKey(
        Producto,
        related_name='ingredientes',
        on_delete=models.PROTECT,
        help_text=_('Producto de la receta'),
    )

    class Meta:
        ordering = ['ingrediente']
        verbose_name = _('Receta')
        verbose_name_plural = _('Recetas')
```

---

## 10. Administración de la Aplicación

### Ejemplo de `admin.py`
Registra tus modelos para gestionarlos desde el panel de administración de Django.

> **Puedes copiar todo este bloque y pegarlo directamente en tu archivo ./src/app/admin.py.**
```python
from django.contrib import admin
from app.models import *

# Register your models here.
admin.site.register(UnidadMedida)
admin.site.register(Ingrediente)
admin.site.register(Barrio)
admin.site.register(Localidad)
admin.site.register(Provincia)
admin.site.register(Cliente)


class RecetaInline(admin.TabularInline):
    model = Receta
    extra = 0


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    inlines = [
        RecetaInline,
    ]
    list_display = (
        'nombre',
        'precio',
        'es_relleno',
    )
    ordering = ['nombre']  # -nombre descendente, nombre ascendente
    search_fields = ['nombre']
    list_filter = (
        'es_relleno',
        'nombre',
    )


class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta
    extra = 0


@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    save_on_top = True
    save_as = True
    list_per_page = 20
    date_hierarchy = 'fecha'
    list_display = (
        'fecha',
        'cliente',
    )

    list_filter = (
        'cliente__nombre',
        'fecha',
    )

    inlines = [
        DetalleVentaInline
    ]
```

---

## 11. Migraciones y Carga de Datos Iniciales

### Realizar migraciones de la app nueva
> **Puedes copiar todo este bloque y pegarlo directamente en tu terminal.**
```bash
docker-compose run --rm manage makemigrations
docker-compose run --rm manage migrate
```

Accede a la administración de Django en [http://localhost:8000/admin/](http://localhost:8000/admin/) donde ya se van a ver los cambios realizados en la app, pero todavía sin datos pre cargados.

### Crear y cargar fixtures (datos iniciales)
Crea la carpeta `./src/app/fixtures` dentro de tu app y agrega el archivo `initial_data.json` con los datos de ejemplo. Luego, carga los datos:

> **Puedes copiar todo este bloque y pegarlo directamente en tu terminal para crear la carpeta.**
```bash
mkdir -p src/app/fixtures
```

> **Puedes copiar todo este bloque y pegarlo directamente en tu archivo ./src/app/fixtures/initial_data.json.**
```json
[
    {
        "model": "app.unidadmedida",
        "pk": 1,
        "fields": {
            "nombre": "KILO"
        }
    },
    {
        "model": "app.unidadmedida",
        "pk": 2,
        "fields": {
            "nombre": "UNIDAD"
        }
    },
    {
        "model": "app.unidadmedida",
        "pk": 3,
        "fields": {
            "nombre": "LITRO"
        }
    },
    {
        "model": "app.ingrediente",
        "pk": 1,
        "fields": {
            "nombre": "HARINA",
            "costo": "150.00",
            "unidad_medida": 1
        }
    },
    {
        "model": "app.ingrediente",
        "pk": 2,
        "fields": {
            "nombre": "SAL",
            "costo": "80.00",
            "unidad_medida": 1
        }
    },
    {
        "model": "app.ingrediente",
        "pk": 3,
        "fields": {
            "nombre": "HUEVO",
            "costo": "25.00",
            "unidad_medida": 2
        }
    },
    {
        "model": "app.ingrediente",
        "pk": 4,
        "fields": {
            "nombre": "JAMÓN",
            "costo": "1200.00",
            "unidad_medida": 1
        }
    },
    {
        "model": "app.ingrediente",
        "pk": 5,
        "fields": {
            "nombre": "QUESO",
            "costo": "800.00",
            "unidad_medida": 1
        }
    },
    {
        "model": "app.ingrediente",
        "pk": 6,
        "fields": {
            "nombre": "ESPINACA",
            "costo": "200.00",
            "unidad_medida": 1
        }
    },
    {
        "model": "app.producto",
        "pk": 1,
        "fields": {
            "nombre": "TALLARIN",
            "ganancia": "2.00",
            "es_relleno": false
        }
    },
    {
        "model": "app.producto",
        "pk": 2,
        "fields": {
            "nombre": "RAVIOLI ESPINACA",
            "ganancia": "3.00",
            "es_relleno": true
        }
    },
    {
        "model": "app.producto",
        "pk": 3,
        "fields": {
            "nombre": "SORRENTINO JAMÓN Y QUESO",
            "ganancia": "3.80",
            "es_relleno": true
        }
    },
    {
        "model": "app.receta",
        "pk": 1,
        "fields": {
            "cantidad": "0.90",
            "ingrediente": 1,
            "producto": 1
        }
    },
    {
        "model": "app.receta",
        "pk": 2,
        "fields": {
            "cantidad": "0.05",
            "ingrediente": 2,
            "producto": 1
        }
    },
    {
        "model": "app.receta",
        "pk": 3,
        "fields": {
            "cantidad": "4.00",
            "ingrediente": 3,
            "producto": 1
        }
    },
    {
        "model": "app.receta",
        "pk": 4,
        "fields": {
            "cantidad": "0.60",
            "ingrediente": 1,
            "producto": 2
        }
    },
    {
        "model": "app.receta",
        "pk": 5,
        "fields": {
            "cantidad": "4.00",
            "ingrediente": 3,
            "producto": 2
        }
    },
    {
        "model": "app.receta",
        "pk": 6,
        "fields": {
            "cantidad": "0.30",
            "ingrediente": 6,
            "producto": 2
        }
    },
    {
        "model": "app.receta",
        "pk": 7,
        "fields": {
            "cantidad": "0.60",
            "ingrediente": 1,
            "producto": 3
        }
    },
    {
        "model": "app.receta",
        "pk": 8,
        "fields": {
            "cantidad": "4.00",
            "ingrediente": 3,
            "producto": 3
        }
    },
    {
        "model": "app.receta",
        "pk": 9,
        "fields": {
            "cantidad": "0.15",
            "ingrediente": 4,
            "producto": 3
        }
    },
    {
        "model": "app.receta",
        "pk": 10,
        "fields": {
            "cantidad": "0.15",
            "ingrediente": 5,
            "producto": 3
        }
    },
    {
        "model": "app.barrio",
        "pk": 1,
        "fields": {
            "nombre": "CENTRO"
        }
    },
    {
        "model": "app.barrio",
        "pk": 2,
        "fields": {
            "nombre": "LAMADRID"
        }
    },
    {
        "model": "app.barrio",
        "pk": 3,
        "fields": {
            "nombre": "AMEGHINO"
        }
    },
    {
        "model": "app.localidad",
        "pk": 1,
        "fields": {
            "nombre": "VILLA MARÍA"
        }
    },
    {
        "model": "app.localidad",
        "pk": 2,
        "fields": {
            "nombre": "VILLA NUEVA"
        }
    },
    {
        "model": "app.provincia",
        "pk": 1,
        "fields": {
            "nombre": "CÓRDOBA"
        }
    },
    {
        "model": "app.cliente",
        "pk": 1,
        "fields": {
            "nombre": "JUAN PÉREZ",
            "numero_documento": 12345678,
            "direccion": "San Martín 123",
            "celular": 3534567890,
            "email": "juan.perez@email.com",
            "barrio": 1,
            "localidad": 1,
            "provincia": 1
        }
    },
    {
        "model": "app.cliente",
        "pk": 2,
        "fields": {
            "nombre": "MARÍA GONZÁLEZ",
            "numero_documento": 87654321,
            "direccion": "Belgrano 456",
            "celular": 3534567891,
            "email": "maria.gonzalez@email.com",
            "barrio": 2,
            "localidad": 1,
            "provincia": 1
        }
    }
]
```

> **Puedes copiar todo este bloque y pegarlo directamente en tu terminal para cargar los datos.**
```bash
docker-compose run --rm manage loaddata initial_data
```

---

## 12. Comandos Útiles

## 12. Comandos Útiles

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
docker-compose run --rm manage makemigrations

# Aplicar migraciones
docker-compose run --rm manage migrate

# Acceder al shell de Django
docker-compose run --rm manage shell

# Recopilar archivos estáticos
docker-compose run --rm manage collectstatic

# Crear superusuario
docker-compose run --rm manage createsuperuser

# Cargar fixtures
docker-compose run --rm manage loaddata initial_data
```

### Cambiar permisos de archivos (Linux/Mac)
> **Puedes copiar todo este bloque y pegarlo directamente en tu terminal.**
```bash
sudo chown $USER:$USER -R .
```

---

## 13. Funcionalidades del Sistema

### Gestión de Productos
- **Sistema de Recetas**: Cada producto puede tener múltiples ingredientes con cantidades específicas
- **Cálculo Automático de Precios**: El precio se calcula automáticamente basado en:
  - Costo de ingredientes × cantidad utilizada
  - Coeficiente de ganancia del producto
- **Clasificación**: Los productos pueden ser marcados como "con relleno" o "sin relleno"

### Gestión de Clientes
- **Información Completa**: Datos personales, contacto y ubicación
- **Ubicación Geográfica**: Provincia → Localidad → Barrio
- **Integración con Usuarios**: Opción de vincular con usuarios del sistema

### Sistema de Ventas
- **Registro de Ventas**: Con fecha y cliente asociado
- **Detalles de Venta**: Productos y cantidades vendidas
- **Trazabilidad**: Seguimiento completo de las transacciones

### Panel de Administración
- **Interfaz Optimizada**: Formularios inline para gestión eficiente
- **Filtros y Búsquedas**: Herramientas avanzadas de navegación
- **Ordenamiento**: Listas organizadas alfabéticamente
- **Paginación**: Manejo eficiente de grandes volúmenes de datos

---

## 14. Estructura de la Base de Datos

El proyecto utiliza PostgreSQL con las siguientes características:

### Modelos Principales
- **NombreAbstract**: Clase base abstracta para modelos con nombre
- **Localidad, Barrio, Provincia**: Jerarquía geográfica
- **UnidadMedida**: Unidades para ingredientes (Kilo, Unidad, Litro)
- **Ingrediente**: Ingredientes con costo y unidad de medida
- **Producto**: Productos finales con ganancia y tipo
- **Receta**: Relación entre productos e ingredientes
- **Cliente**: Información completa de clientes
- **Venta**: Transacciones de venta
- **DetalleVenta**: Detalles de cada venta

### Relaciones
- **Producto ↔ Ingrediente**: Relación many-to-many a través de Receta
- **Cliente → Ubicación**: ForeignKey a Provincia, Localidad, Barrio
- **Venta → Cliente**: ForeignKey con protección
- **DetalleVenta → Venta/Producto**: ForeignKey con protección

### Características Técnicas
- **Índices Optimizados**: Para consultas frecuentes
- **Validaciones**: A nivel de modelo y base de datos
- **Eliminación Protegida**: PROTECT en relaciones críticas
- **Eliminación en Cascada**: CASCADE donde es apropiado
- **Valores Nulos Controlados**: SET_NULL para datos opcionales

---

## 15. Desarrollo y Personalización

### Extensión del Proyecto
Puedes extender el proyecto agregando:

#### Nuevos Modelos
> **Ejemplo de nuevo modelo en ./src/app/models.py:**
```python
class Categoria(NombreAbstract):
    descripcion = models.TextField(
        _('Descripción'),
        help_text=_('Descripción de la categoría'),
        blank=True,
        null=True
    )
    
    class Meta:
        verbose_name = 'categoría'
        verbose_name_plural = 'categorías'
```

#### Configuración de Admin
> **Ejemplo de configuración en ./src/app/admin.py:**
```python
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ['nombre']
    ordering = ['nombre']
```

#### Vistas Personalizadas
> **Ejemplo de vista en ./src/app/views.py:**
```python
from django.shortcuts import render
from django.http import JsonResponse
from .models import Producto

def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'app/productos.html', {'productos': productos})

def precio_producto(request, producto_id):
    try:
        producto = Producto.objects.get(id=producto_id)
        return JsonResponse({'precio': producto.precio})
    except Producto.DoesNotExist:
        return JsonResponse({'error': 'Producto no encontrado'}, status=404)
```

#### URLs Personalizadas
> **Ejemplo de configuración en ./src/app/urls.py:**
```python
from django.urls import path
from . import views

urlpatterns = [
    path('productos/', views.lista_productos, name='lista_productos'),
    path('producto/<int:producto_id>/precio/', views.precio_producto, name='precio_producto'),
]
```

### Comandos de Desarrollo
> **Comandos útiles para desarrollo:**
```bash
# Crear migraciones para cambios específicos
docker-compose run --rm manage makemigrations app

# Ver SQL de las migraciones
docker-compose run --rm manage sqlmigrate app 0001

# Verificar problemas en el proyecto
docker-compose run --rm manage check

# Ejecutar tests
docker-compose run --rm manage test

# Abrir shell de Django
docker-compose run --rm manage shell

# Crear datos de prueba
docker-compose run --rm manage shell -c "
from app.models import *
from django.contrib.auth.models import User

# Crear datos de ejemplo
provincia = Provincia.objects.create(nombre='Buenos Aires')
localidad = Localidad.objects.create(nombre='La Plata')
barrio = Barrio.objects.create(nombre='Centro')
"
```

---

## 16. Solución de Problemas Comunes

### Problemas de Conexión a la Base de Datos
```bash
# Verificar estado de los contenedores
docker-compose ps

# Ver logs de la base de datos
docker-compose logs db

# Reiniciar servicios
docker-compose restart
```

### Problemas de Permisos (Linux/Mac)
```bash
# Cambiar propietario de archivos
sudo chown -R $USER:$USER .

# Dar permisos de escritura
chmod -R 755 .
```

### Problemas de Migraciones
```bash
# Ver estado de las migraciones
docker-compose run --rm manage showmigrations

# Aplicar migraciones específicas
docker-compose run --rm manage migrate app 0001

# Revertir migraciones
docker-compose run --rm manage migrate app zero
```

### Limpiar y Reconstruir
```bash
# Limpiar completamente
docker-compose down -v --remove-orphans --rmi all
docker system prune -a

# Reconstruir desde cero
docker-compose build --no-cache
docker-compose up -d
```

---

## 17. Mejores Prácticas

### Desarrollo
- **Usar migraciones**: Nunca modifiques la base de datos directamente
- **Validar modelos**: Usar `clean()` y `full_clean()` en los modelos
- **Documentar código**: Usar docstrings y comentarios
- **Manejo de errores**: Usar try/except apropiadamente

### Producción
- **Variables de entorno**: Usar `.env` para configuraciones sensibles
- **Logs**: Configurar logging apropiado
- **Backup**: Hacer respaldos regulares de la base de datos
- **Monitoreo**: Implementar monitoreo de salud de la aplicación

### Seguridad
- **DEBUG = False**: En producción
- **SECRET_KEY**: Usar una clave secreta única y segura
- **ALLOWED_HOSTS**: Configurar hosts permitidos
- **HTTPS**: Usar conexiones seguras en producción

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
