from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    ES_PROFESOR = 'PR'
    ES_ALUMNO = 'AL'
    ROLES = [
        (ES_PROFESOR, 'Profesor'),
        (ES_ALUMNO, 'Alumno'),
    ]
    rol = models.CharField(max_length=2, choices=ROLES, default=ES_ALUMNO)

    def __str__(self):
        return f"{self.username} ({self.get_rol_display()})"
    

class Tarea(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha_limite = models.DateTimeField()
    creado_por = models.ForeignKey('Usuario', on_delete=models.CASCADE, related_name='tareas_creadas')
    finalizada = models.BooleanField(default=False)
    requiere_evaluacion = models.BooleanField(default=False)

    def __str__(self):
        return self.titulo

class TareaIndividual(Tarea):
    alumno_asignado = models.ForeignKey('Usuario', on_delete=models.CASCADE, related_name='tareas_individuales')

class TareaGrupal(Tarea):
    alumnos = models.ManyToManyField('Usuario', related_name='tareas_grupales')