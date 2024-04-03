from django.contrib import admin
from .models import dbElementos
from .models import dbCombinaciones

# Aquí registramos las tablas de la base de datos para que se puedan administrar
admin.site.register(dbElementos)
admin.site.register(dbCombinaciones)
