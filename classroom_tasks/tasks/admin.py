from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    # Columnas visibles en el listado de tareas
    list_display = ("title", "type", "status", "creator", "requires_teacher_validation", "due_date", "created_at")
    list_filter = ("type", "status", "requires_teacher_validation")
    search_fields = ("title", "description")

    # Para ver los miembros en detalle
    filter_horizontal = ("members",)
