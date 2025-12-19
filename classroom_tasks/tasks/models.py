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
    title = models.CharField("Título", max_length=120)

    # Descripción opcional de la tarea.
    description = models.TextField("Descripción", blank=True)

    # Tipo de tarea, limitado a las opciones definidas en TYPE_CHOICES.
    type = models.CharField("Tipo", max_length=20, choices=TYPE_CHOICES)

    # Indica si la tarea requiere validación por parte de un profesor.
    requires_teacher_validation = models.BooleanField("Requiere validación del profesor", 
                                                      default=False)

    # Usuario creador de la tarea (normalmente un profesor).
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Creador",
        on_delete=models.CASCADE,
        related_name='created_tasks'
    ) 

    # Miembros asociados a la tarea (alumnos que participan).
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name="Miembros",
        related_name='collaborating_tasks',
        blank=True
    )

    # Fecha límite de entrega (opcional).
    due_date= models.DateTimeField("Fecha límite", null=True, blank=True)

    # Fecha de la creación de la tarea (se asigna automáticamente).
    created_at = models.DateTimeField("Fecha de creación", auto_now_add=True)

    # Estado actual de la tarea, limitado a STATUS_CHOICES. 
    status = models.CharField("Estado",
             max_length=20,
             choices=STATUS_CHOICES,
             default='PENDIENTE'
        )
    
    # Profesor que valida la tarea (puede ser nulo si no se ha asignado).
    teacher_validator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Profesor validador",
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='tasks_to_validate'
    )

    

    # Representación en texto de la tarea (útil en el admin y en depuración).
    def __str__(self):
        return f'{self.title} ({self.type})'  
        # Métodos auxiliares
    def is_pending(self):
        return self.status == 'PENDIENTE'

    def is_delivered(self):
        return self.status == 'ENTREGADA'

    def is_validated(self):
        return self.status == 'VALIDADA'

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Tarea"
        verbose_name_plural = "Tareas"