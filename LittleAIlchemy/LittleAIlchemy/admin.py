from django.contrib import admin
from .models import dbElementos
from .models import dbCombinaciones

admin.site.register(dbElementos)
admin.site.register(dbCombinaciones)
