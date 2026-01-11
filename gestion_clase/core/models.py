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