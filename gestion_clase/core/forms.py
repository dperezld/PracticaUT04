from django import forms
from django.utils import timezone
from .models import TareaIndividual, TareaGrupal, Usuario

# --- FORMULARIO DE ALTA DE USUARIOS (NUEVO) ---
class RegistroUsuarioForm(forms.ModelForm):
    # Definimos el campo password manualmente para que sea de tipo contraseña
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mínimo 8 caracteres'})
    )

    class Meta:
        model = Usuario
        fields = ['username', 'first_name', 'last_name', 'email', 'rol', 'password']
        labels = {
            'username': 'Nombre de usuario',
            'first_name': 'Nombre',
            'last_name': 'Apellidos',
            'email': 'Correo electrónico',
            'rol': 'Tipo de usuario (Rol)',
        }
        # Añadimos clases CSS para que se vea profesional con tu style.css
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'rol': forms.Select(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        # Sobrescribimos el save para encriptar la contraseña correctamente
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

# --- FORMULARIO TAREA INDIVIDUAL ---
class TareaIndividualForm(forms.ModelForm):
    class Meta:
        model = TareaIndividual
        fields = ['titulo', 'descripcion', 'alumno_asignado', 'fecha_limite', 'requiere_evaluacion']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'alumno_asignado': forms.Select(attrs={'class': 'form-control'}),
            'fecha_limite': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'requiere_evaluacion': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_fecha_limite(self):
        fecha = self.cleaned_data.get('fecha_limite')
        if fecha and fecha < timezone.now():
            raise forms.ValidationError("La fecha límite no puede ser anterior a hoy.")
        return fecha

# --- FORMULARIO TAREA GRUPAL ---
class TareaGrupalForm(forms.ModelForm):
    class Meta:
        model = TareaGrupal
        fields = ['titulo', 'descripcion', 'alumnos', 'fecha_limite', 'requiere_evaluacion']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'alumnos': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'fecha_limite': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'requiere_evaluacion': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_alumnos(self):
        alumnos = self.cleaned_data.get('alumnos')
        if alumnos and alumnos.count() < 2:
            raise forms.ValidationError("Una tarea grupal debe tener al menos 2 alumnos.")
        return alumnos