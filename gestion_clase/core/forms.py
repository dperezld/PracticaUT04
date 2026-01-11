from django import forms
from django.utils import timezone
from .models import TareaIndividual, TareaGrupal

class TareaIndividualForm(forms.ModelForm):
    class Meta:
        model = TareaIndividual
        fields = ['titulo', 'descripcion', 'alumno_asignado', 'fecha_limite', 'requiere_evaluacion']

    def clean_fecha_limite(self):
        fecha = self.cleaned_data.get('fecha_limite')
        if fecha and fecha < timezone.now():
            raise forms.ValidationError("La fecha límite no puede ser anterior a hoy.")
        return fecha

class TareaGrupalForm(forms.ModelForm):
    class Meta:
        model = TareaGrupal
        fields = ['titulo', 'descripcion', 'alumnos', 'fecha_limite', 'requiere_evaluacion']

    def clean_alumnos(self):
        alumnos = self.cleaned_data.get('alumnos')
        if alumnos and alumnos.count() < 2:
            raise forms.ValidationError("Una tarea grupal debe tener al menos 2 alumnos.")
        return alumnos