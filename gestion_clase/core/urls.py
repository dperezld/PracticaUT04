from django.urls import path
from .views import MisTareasView, TareasPendientesProfesorView

urlpatterns = [
    path('mis-tareas/', MisTareasView.as_view(), name='mis_tareas'),
    path('tareas-profesor/', TareasPendientesProfesorView.as_view(), name='tareas_profesor'),
]