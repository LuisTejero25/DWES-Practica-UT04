from django.db import models
from django.conf import settings

class Task(models.Model):
    # Tipos de tarea disponibles (individual, grupal y evaluable)
    TYPE_CHOICES = [
        ('INDIVIDUAL', 'Individual'),   # Tarea realizada por un único alumno
        ('GRUPAL', 'Grupal'),           # Tarea realizada por varios alumnos
        ('EVALUABLE', 'Evaluable'),     # Tarea quee requiere validación del profesor
                            
    ]

    # Estados posibles de una tarea
    STATUS_CHOICES = [
        ('PENDIENTE', 'Pendiente'),     # Tarea creada pero no entregada
        ('ENTREGADA', 'Entregada'),     # Tarea entregada por alumno o grupo
        ('VALIDADA', 'Validada'),       # Tarea validada por el profesor
        ('COMPLETADA', 'Completada'),   # Tarea marcada como completada por el alumno
    ]

    title = models.CharField(
        "Título",
        max_length=120
    )  # Título de la tarea

    description = models.TextField(
        "Descripción",
        blank=True
    )  # Descripción opcional

    type = models.CharField(
        "Tipo",
        max_length=20,
        choices=TYPE_CHOICES,
        blank=True
    )  # Tipo de tarea (se asigna en el formulario)

    requires_teacher_validation = models.BooleanField(
        "Requiere validación del profesor",
        default=False
    )  # Indica si necesita validación del profesor

    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Creador",
        on_delete=models.CASCADE,
        related_name='created_tasks'
    )  # Usuario que crea la tarea

    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name="Miembros",
        related_name='collaborating_tasks',
        blank=True
    )  # Alumnos que participan en la tarea (solo en grupales)

    due_date = models.DateTimeField(
        "Fecha límite",
        null=True,
        blank=True
    )  # Fecha límite de entrega

    created_at = models.DateTimeField(
        "Fecha de creación",
        auto_now_add=True
    )  # Fecha en la que se creó la tarea

    status = models.CharField(
        "Estado",
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDIENTE'
    )  # Estado actual de la tarea

    teacher_validator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Profesor validador",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tasks_to_validate'
    )  # Profesor que valida la tarea (si aplica)

    delivery_file = models.FileField(
        "Archivo de entrega",
        upload_to="deliveries/",
        null=True,
        blank=True
    )  # Archivo PDF entregado por el alumno

    delivery_date = models.DateTimeField(
        "Fecha de entrega",
        null=True,
        blank=True
    )  # Fecha en la que el alumno entrega la tarea

    def __str__(self):
        return f"{self.title} ({self.type})"  # Representación legible en admin

    class Meta:
        ordering = ['-created_at']  # Ordenar por fecha de creación descendente
        verbose_name = "Tarea"
        verbose_name_plural = "Tareas"
