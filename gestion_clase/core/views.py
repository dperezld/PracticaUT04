from django.views.generic import ListView
from .models import Tarea, TareaIndividual, TareaGrupal
from django.db.models import Q

# Vista para que el alumno vea sus tareas (individuales y grupales)
class MisTareasView(ListView):
    model = Tarea
    template_name = 'core/mis_tareas.html'
    context_object_name = 'tareas'

    def get_queryset(self):
        u = self.request.user
        # Filtramos tareas donde el usuario es el asignado o está en el grupo
        return Tarea.objects.filter(
            Q(tareaindividual__alumno_assigned=u) | 
            Q(tareagrupal__alumnos=u)
        ).distinct()

# Vista para que el profesor vea tareas que requieren validación
class TareasPendientesProfesorView(ListView):
    model = Tarea
    template_name = 'core/tareas_profesor.html'
    context_object_name = 'tareas'

    def get_queryset(self):
        return Tarea.objects.filter(requiere_evaluacion=True, finalizada=False)