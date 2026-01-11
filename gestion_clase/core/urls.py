from django.urls import path
from .views import (
    MisTareasView, 
    TareasPendientesProfesorView, 
    PerfilUsuarioView,
    ListaUsuariosView,
    RegistroUsuarioView,
    TareaIndividualCreateView,
    TareaGrupalCreateView
)
from . import views

urlpatterns = [
    # --- Tareas (Visualización y Acción) ---
    path('mis-tareas/', MisTareasView.as_view(), name='mis_tareas'),
    path('tareas-profesor/', TareasPendientesProfesorView.as_view(), name='tareas_profesor'),
    path('finalizar/<int:pk>/', views.finalizar_tarea, name='finalizar_tarea'),

    # --- Usuarios (Perfil y Listados) ---
    path('perfil/', PerfilUsuarioView.as_view(), name='perfil'),
    path('usuarios/', ListaUsuariosView.as_view(), name='lista_usuarios'),
    path('registro/', RegistroUsuarioView.as_view(), name='registro'),

    # --- Creación de Tareas ---
    path('nueva-individual/', TareaIndividualCreateView.as_view(), name='nueva_individual'),
    path('nueva-grupal/', TareaGrupalCreateView.as_view(), name='nueva_grupal'),
]