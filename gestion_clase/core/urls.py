from django.urls import path
from .views import MisTareasView, TareasPendientesProfesorView
from . import views

urlpatterns = [
    path('mis-tareas/', MisTareasView.as_view(), name='mis_tareas'),
    path('tareas-profesor/', TareasPendientesProfesorView.as_view(), name='tareas_profesor'),
    path('finalizar/<int:pk>/', views.finalizar_tarea, name='finalizar_tarea'),
]