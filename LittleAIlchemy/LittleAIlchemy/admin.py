from django.contrib import admin
from .models import dbElementos, dbCombinaciones, victorias

# Aquí registramos las tablas de la base de datos para que se puedan administrar
admin.site.register(dbElementos)
admin.site.register(dbCombinaciones)
admin.site.register(victorias)
