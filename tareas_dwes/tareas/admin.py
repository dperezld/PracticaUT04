from django.contrib import admin
# Importamos tu modelo Tarea desde el archivo models.py
from .models import Tarea

# Le decimos al admin que "registre" (muestre) este modelo
admin.site.register(Tarea)