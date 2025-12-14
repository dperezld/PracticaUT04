import uuid
from django.db import models

class Tarea(models.Model):
    # UUIDField es más seguro y único que un ID numérico simple
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    titulo = models.CharField(max_length=200, verbose_name="Título")
    descripcion = models.TextField(verbose_name="Descripción")
    
    # Por defecto la tarea no está completada
    completada = models.BooleanField(default=False)
    
    # auto_now_add guarda la fecha exacta en que se crea el objeto
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    # Fecha recordatorio manual. null=True permite que esté vacío en la BD si no se define.
    fecha_recordatorio = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.titulo