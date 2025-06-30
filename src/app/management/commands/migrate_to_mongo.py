from django.apps import apps
from django.core.management.base import BaseCommand
from django.db import transaction


class Command(BaseCommand):
    help = "Migra todos los datos de old_db (PostgreSQL) a default (MongoDB)"

    def handle(self, *args, **kwargs):
        app_label = "app"
        models = apps.get_app_config(app_label).get_models()
        self.stdout.write(self.style.SUCCESS("Iniciando migración de datos..."))

        # Opcional: ordena los modelos para primero migrar los que no tienen FKs
        models = sorted(models, key=lambda m: len(m._meta.fields))

        for model in models:
            model_name = model.__name__
            self.stdout.write(f"Migrando modelo: {model_name}")

            # Obtiene todos los objetos de old_db
            objs = list(model.objects.using("old_db").all())
            total = len(objs)
            if total == 0:
                self.stdout.write(f"  No hay datos para migrar en {model_name}.")
                continue

            migrated = 0
            for obj in objs:
                # Clona el objeto
                obj.pk = obj.pk  # Conserva el PK si es posible
                obj._state.db = "default"  # Cambia el estado a la nueva DB
                try:
                    obj.save(using="default", force_insert=True)
                    migrated += 1
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"  Error migrando {obj}: {e}"))
            self.stdout.write(
                self.style.SUCCESS(
                    f"  Migrados {migrated}/{total} objetos de {model_name}"
                )
            )

        self.stdout.write(self.style.SUCCESS("¡Migración completa!"))
