from django.urls import path  # Sistema de rutas
from . import views           # Importamos las vistas de la app

app_name = "tasks"  # Namespace de la app

urlpatterns = [
    path('', views.list_my_tasks, name='tasks_home'),
    path('create/', views.create_task, name='create_task'),  # Crear una nueva tarea
    path('mine/', views.list_my_tasks, name='list_my_tasks'),  # Tareas creadas o en las que participa el usuario
    path('to-validate/', views.tasks_to_validate, name='tasks_to_validate'),  # Tareas pendientes de validación por el profesor

    path('<int:task_id>/deliver/', views.deliver_task, name='deliver_task'),  # Entregar una tarea
    path('<int:task_id>/validate/', views.validate_task, name='validate_task'),  # Validación por parte del profesor
    path('<int:task_id>/cancel/', views.cancel_delivery, name='cancel_delivery'),  # Cancelar entrega
    path('validate-by-student/<int:task_id>/', views.validate_task_by_student, name='validate_by_student'),  # Validación por alumno

    path('<int:task_id>/', views.task_detail, name='detail'),  # Detalle de una tarea (siempre al final)
]
