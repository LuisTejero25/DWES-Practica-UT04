from django import forms  # Módulo de formularios de Django
from django.contrib.auth.forms import UserCreationForm  # Formulario base para crear usuarios
from accounts.models import User  # Importamos nuestro modelo de usuario personalizado


class CustomUserCreationForm(UserCreationForm):
   
    # Campo 'role' declarado explícitamente para asegurar validación correcta
    role = forms.ChoiceField(
        choices=User.ROLE_CHOICES,  # Opciones definidas en el modelo (student / teacher)
        required=True,              # Obligamos a seleccionar un rol (evita errores silenciosos)
        widget=forms.Select(attrs={"class": "form-control"})  # Estilo coherente con el proyecto
    )

    class Meta:
        model = User  # Indicamos que este formulario trabaja con nuestro modelo User
        fields = [
            "username",   # Nombre de usuario
            "email",      # Correo electrónico
            "role",       # Rol del usuario (student / teacher)
            "password1",  # Contraseña
            "password2",  # Confirmación de contraseña
        ]

        # Widgets para aplicar estilos visuales a los campos
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }
