from django.views.generic import ListView
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Q
from .models import Tarea, TareaIndividual, TareaGrupal

# Vista para que el alumno vea sus tareas (individuales y grupales)
class MisTareasView(ListView):
    model = Tarea
    template_name = 'core/mis_tareas.html'
    context_object_name = 'tareas'

    def get_queryset(self):
        u = self.request.user
        # Filtramos tareas donde el usuario es el asignado o está en el grupo
        return Tarea.objects.filter(
            Q(tareaindividual__alumno_asignado=u) | 
            Q(tareagrupal__alumnos=u)
        ).distinct()

# Vista para que el profesor vea tareas que requieren validación
class TareasPendientesProfesorView(ListView):
    model = Tarea
    template_name = 'core/tareas_profesor.html'
    context_object_name = 'tareas'

    def get_queryset(self):
        return Tarea.objects.filter(requiere_evaluacion=True, finalizada=False)

# Nueva función para marcar tareas como terminadas
def finalizar_tarea(request, pk):
    tarea = get_object_or_404(Tarea, pk=pk)
    
    # Lógica de validación:
    # Si requiere evaluación, solo el profesor (PR) puede finalizarla.
    if tarea.requiere_evaluacion:
        if hasattr(request.user, 'rol') and request.user.rol == 'PR':
            tarea.finalizada = True
    else:
        # Si no requiere evaluación, el alumno puede marcarla como hecha.
        tarea.finalizada = True
        
    tarea.save()
    return redirect('mis_tareas')