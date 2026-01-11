from django.views.generic import ListView
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.contrib.auth.decorators import login_required
from .models import Tarea, TareaIndividual, TareaGrupal

# --- PORTERO DE REDIRECCIÓN ÚNICO ---
@login_required
def root_redirect(request):
    """
    Esta es la función que decide el destino tras el login único.
    """
    # Si el usuario tiene rol de Profesor ('PR'), lo mandamos a su panel de validación
    if hasattr(request.user, 'rol') and request.user.rol == 'PR':
        return redirect('tareas_profesor') 
    # Los alumnos van a su lista personal
    return redirect('mis_tareas') 

class MisTareasView(LoginRequiredMixin, ListView):
    model = Tarea
    template_name = 'core/mis_tareas.html'
    context_object_name = 'tareas'
    login_url = '/login/'  

    def get_queryset(self):
        u = self.request.user
        return Tarea.objects.filter(
            Q(tareaindividual__alumno_asignado=u) | 
            Q(tareagrupal__alumnos=u)
        ).distinct()

class TareasPendientesProfesorView(LoginRequiredMixin, ListView):
    model = Tarea
    template_name = 'core/tareas_profesor.html'
    context_object_name = 'tareas'
    login_url = '/login/'

    def get_queryset(self):
        # El profesor solo ve tareas que requieren su evaluación y no han terminado
        return Tarea.objects.filter(requiere_evaluacion=True, finalizada=False)

def finalizar_tarea(request, pk):
    if not request.user.is_authenticated:
        return redirect('/login/')
        
    tarea = get_object_or_404(Tarea, pk=pk)
    
    # Marcamos como finalizada
    if hasattr(request.user, 'rol'):
        if request.user.rol == 'PR':
            tarea.finalizada = True
        elif request.user.rol == 'AL' and not tarea.requiere_evaluacion:
            tarea.finalizada = True
    
    tarea.save() # Guardamos en PostgreSQL
    
    # --- REDIRECCIÓN FORZADA ---
    if hasattr(request.user, 'rol') and request.user.rol == 'PR':
        print(f"DEBUG: El usuario {request.user.username} es PROFESOR. Redirigiendo a panel profesor.")
        return redirect('tareas_profesor')
    else:
        print(f"DEBUG: El usuario {request.user.username} es ALUMNO. Redirigiendo a mis tareas.")
        return redirect('mis_tareas')