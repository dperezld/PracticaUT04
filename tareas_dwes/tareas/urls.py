from django.urls import path
from .views import TareaDetailView

urlpatterns = [
    # Usamos <uuid:pk> porque tu ID es un UUID, no un entero (<int:pk>)
    path('tarea/<uuid:pk>/', TareaDetailView.as_view(), name='detalle_tarea'),
]