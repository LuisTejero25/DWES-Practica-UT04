from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Definimos las opciones de rol disponibles.
    ROLE_CHOICES = [
        ('ALUMNO', 'Alumno'),    # Rol para estudiantes
        ('PROFESOR', 'Profesor') # Rol para profesores
    ]

    # Se limita a las opciones definidas en ROLE_CHOICES.
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    # Método auxiliar para comprobar si el usuario es alumno.
    def is_alumno(self):
        return self.role == 'ALUMNO'

    # Método auxiliar para comprobar si el usuario es profesor.
    def is_profesor(self):
        return self.role == 'PROFESOR'
