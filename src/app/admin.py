from django.contrib import admin

from .models import *

admin.site.register(Cliente)
admin.site.register(TipoDNI)
admin.site.register(MedioDePago)
admin.site.register(Evento)
admin.site.register(Entrada)
admin.site.register(Venta)
admin.site.register(DetalleDeVenta)
