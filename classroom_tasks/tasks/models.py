from django.db import models
from django.conf import settings

class Task(models.Model):
    # Tipos de tareas disponibles.
    TYPE_CHOICES = [
        ('INDIVIDUAL', 'Individual'), # Tarea realizada por un único alumno.
        ('GRUPAL', 'Grupal'), # Tarea realizada en grupo.
        ('EVALUABLE', 'Evaluable'), #Tarea que cuenta para evaluación.
    ]

    # Posibles estados de una tarea.
    STATUS_CHOICES = [
        ('PENDIENTE', 'Pendiente'), # Tarea creada pero aún no entregada.
        ('ENTREGADA', 'Entregada'), # Tarea entregada por un alumno o un grupo.
        ('VALIDADA', 'Validada'), # Tarea revisada y validada por el profesor.
    ]

    # Título de la tarea (obligatorio y maximo 120 caracteres).
    title = models.CharField(max_length=120)

    # Descripción opcional de la tarea.
    description = models.TextField(blank=True)

    # Tipo de tarea, limitado a las opciones definidas en TYPE_CHOICES.
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)

    # Indica si la tarea requiere validación por parte de un profesor.
    requires_teacher_validation = models.BooleanField(default=False)

    # Usuario creador de la tarea (normalmente un profesor).
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_tasks'
    ) 

    # Miembros asociados a la tarea (alumnos que participan).
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='member_tasks',
        blank=True
    )

    # Fecha límite de entrega (opcional).
    due_date= models.DateTimeField(null=True, blank=True)

    # Fecha de la creación de la tarea (se asigna automáticamente).
    created_at = models.DateTimeField(auto_now_add=True)

    # Estado actual de la tarea, limitado a STATUS_CHOICES. 
    status = models.CharField(
             max_length=10,
             choices=STATUS_CHOICES,
             default='PENDIENTE'
        )
    
    # Profesor que valida la tarea (puede ser nulo si no se ha asignado).
    teacher_validator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='tasks_to_validate'
    )

    # Representación en texto de la tarea (útil en el admin y en depuración).
    def __str__(self):
        return f'{self.title} ({self.type})'  