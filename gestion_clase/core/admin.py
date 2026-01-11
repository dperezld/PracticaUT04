from django.contrib import admin
from .models import Usuario, TareaIndividual, TareaGrupal

admin.site.register(Usuario)
admin.site.register(TareaIndividual)
admin.site.register(TareaGrupal)