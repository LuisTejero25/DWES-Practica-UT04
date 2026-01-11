from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Opciones de rol disponibles en el sistema
    ROLE_CHOICES = [
        ('student', 'Alumno'),     # Rol para estudiantes
        ('teacher', 'Profesor'),   # Rol para profesores
    ]

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        blank=True,                # Permite crear usuarios sin rol inicial
        default='student'          # Valor por defecto
    )  # Rol del usuario dentro de la plataforma

    # Método auxiliar para comprobar si el usuario es alumno
    def is_alumno(self):
        return self.role == 'student'

    # Método auxiliar para comprobar si el usuario es profesor
    def is_profesor(self):
        return self.role == 'teacher'
