
import os
import django
import sys
from django.utils import timezone
from datetime import timedelta

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_clase.settings')
django.setup()

from core.models import Usuario, TareaIndividual, TareaGrupal
from django.contrib.auth import get_user_model

def populate():
    User = get_user_model()
    
    # 1. Crear Superusuario (Profesor)
    if not User.objects.filter(username='admin').exists():
        admin = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        admin.rol = Usuario.ES_PROFESOR
        admin.save()
        print("Superusuario 'admin' (password: admin123) creado.")
    else:
        admin = User.objects.get(username='admin')
        print("Superusuario 'admin' ya existe.")

    # 2. Crear Alumnos
    alumno1, _ = User.objects.get_or_create(username='alumno1', defaults={'rol': Usuario.ES_ALUMNO})
    alumno1.set_password('alumno123')
    alumno1.save()
    
    alumno2, _ = User.objects.get_or_create(username='alumno2', defaults={'rol': Usuario.ES_ALUMNO})
    alumno2.set_password('alumno123')
    alumno2.save()
    
    print("Alumnos 'alumno1' y 'alumno2' (password: alumno123) listos.")

    # 3. Crear Tareas
    # Tarea Individual
    if not TareaIndividual.objects.filter(titulo='Tarea 1 Individual').exists():
        TareaIndividual.objects.create(
            titulo='Tarea 1 Individual',
            descripcion='Descripción de prueba individual',
            fecha_limite=timezone.now() + timedelta(days=7),
            creado_por=admin,
            alumno_asignado=alumno1,
            requiere_evaluacion=True
        )
        print("Tarea Individual creada.")

    # Tarea Grupal
    if not TareaGrupal.objects.filter(titulo='Tarea 1 Grupal').exists():
        tg = TareaGrupal.objects.create(
            titulo='Tarea 1 Grupal',
            descripcion='Trabajo en equipo',
            fecha_limite=timezone.now() + timedelta(days=10),
            creado_por=admin,
            requiere_evaluacion=True
        )
        tg.alumnos.add(alumno1, alumno2)
        print("Tarea Grupal creada.")

if __name__ == '__main__':
    populate()
