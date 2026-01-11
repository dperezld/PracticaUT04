from django.views.generic import ListView, DetailView, CreateView
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.contrib.auth.decorators import login_required
from .models import Tarea, TareaIndividual, TareaGrupal, Usuario
from .forms import RegistroUsuarioForm, TareaIndividualForm, TareaGrupalForm

# --- PORTERO DE REDIRECCIÓN ÚNICO ---
@login_required
def root_redirect(request):
    if hasattr(request.user, 'rol') and request.user.rol == 'PR':
        return redirect('tareas_profesor') 
    return redirect('mis_tareas') 

# --- VISTAS DE TAREAS (EXISTENTES) ---
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
        return Tarea.objects.filter(requiere_evaluacion=True, finalizada=False)

# --- NUEVA VISTA: Perfil de Usuario (Ver sus propios datos) ---
class PerfilUsuarioView(LoginRequiredMixin, DetailView):
    model = Usuario
    template_name = 'core/perfil.html'
    context_object_name = 'perfil'

    def get_object(self):
        return self.request.user

# --- NUEVA VISTA: Listado de todo el alumnado/profesorado ---
class ListaUsuariosView(LoginRequiredMixin, ListView):
    model = Usuario
    template_name = 'core/lista_usuarios.html'
    context_object_name = 'usuarios'

# --- NUEVA VISTA: Formulario para el alta del alumnado/profesorado ---
class RegistroUsuarioView(LoginRequiredMixin, CreateView):
    model = Usuario
    form_class = RegistroUsuarioForm
    template_name = 'core/form_generico.html'
    success_url = reverse_lazy('lista_usuarios')

    def dispatch(self, request, *args, **kwargs):
        # Opcional: Solo permitir que profesores creen otros usuarios
        if not request.user.rol == 'PR':
            return redirect('mis_tareas')
        return super().dispatch(request, *args, **kwargs)

# --- NUEVAS VISTAS: Creación de Tareas (Individual y Grupal) ---
class TareaIndividualCreateView(LoginRequiredMixin, CreateView):
    model = TareaIndividual
    form_class = TareaIndividualForm
    template_name = 'core/form_generico.html'
    success_url = reverse_lazy('mis_tareas')

class TareaGrupalCreateView(LoginRequiredMixin, CreateView):
    model = TareaGrupal
    form_class = TareaGrupalForm
    template_name = 'core/form_generico.html'
    success_url = reverse_lazy('mis_tareas')

# --- ACCIÓN: Finalizar Tarea ---
def finalizar_tarea(request, pk):
    if not request.user.is_authenticated:
        return redirect('/login/')
        
    tarea = get_object_or_404(Tarea, pk=pk)
    
    if hasattr(request.user, 'rol'):
        if request.user.rol == 'PR':
            tarea.finalizada = True
        elif request.user.rol == 'AL' and not tarea.requiere_evaluacion:
            tarea.finalizada = True
    
    tarea.save()
    
    if hasattr(request.user, 'rol') and request.user.rol == 'PR':
        return redirect('tareas_profesor')
    else:
        return redirect('mis_tareas')