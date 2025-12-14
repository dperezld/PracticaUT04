from django.shortcuts import render

from django.views.generic import DetailView
from .models import Tarea

class TareaDetailView(DetailView):
    model = Tarea
    template_name = 'tareas/detalle_tarea.html' # Ruta donde buscaremos el HTML
    context_object_name = 'tarea' # Nombre de la variable a usar en el HTML