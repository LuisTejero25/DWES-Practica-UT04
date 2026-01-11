from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Task
from .forms import IndividualTaskForm, GroupTaskForm, TaskDeliveryForm as DeliverTaskForm


# Crear una nueva tarea (alumno o profesor)
@login_required
def create_task(request):
    # Elegimos el formulario según el parámetro GET
    task_type = request.GET.get("type", "individual")

    FormClass = GroupTaskForm if task_type == "group" else IndividualTaskForm

    if request.method == 'POST':
        form = FormClass(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.type = task_type.upper()          # tipo de tarea 
            task.creator = request.user            # Usuario que crea la tarea
            task.status = 'PENDIENTE'              # Estado inicial
            task.save()

            if task_type == "group":
                form.save_m2m()                    # Guardar miembros

            messages.success(request, 'Tarea creada correctamente.')
            return redirect("tasks:list_my_tasks")
    else:
        form = FormClass()

    return render(request, 'tasks/create_task.html', {
        'form': form,
        'task_type': task_type
    })


# Listar tareas del usuario (creadas y colaboradas)
@login_required
def list_my_tasks(request):
    created = Task.objects.filter(creator=request.user).distinct()
    collaborating = Task.objects.filter(members=request.user).exclude(creator=request.user).distinct()

    return render(request, 'tasks/list_my_tasks.html', {
        'created': created,
        'collaborating': collaborating
    })


# Listar tareas que requieren validación del profesor
@login_required
def tasks_to_validate(request):
    # Solo profesores o admin pueden acceder
    if request.user.role != "teacher" and not request.user.is_superuser:
        messages.error(request, "No tienes permisos para validar tareas.")
        return redirect("tasks:list_my_tasks")

    tasks = Task.objects.filter(
        requires_teacher_validation=True,
        status='ENTREGADA'
    )

    return render(request, 'tasks/tasks_to_validate.html', {'tasks': tasks})


# Entregar una tarea (alumno)
@login_required
def deliver_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    # Solo creador o miembros pueden entregar
    if task.creator != request.user and not task.members.filter(id=request.user.id).exists():
        messages.error(request, 'No tienes permisos para entregar esta tarea.')
        return redirect("tasks:list_my_tasks")

    # Solo se puede entregar si está pendiente
    if task.status != 'PENDIENTE':
        messages.warning(request, 'La tarea no está en estado pendiente.')
        return redirect("tasks:list_my_tasks")

    if request.method == "POST":
        form = DeliverTaskForm(request.POST, request.FILES, instance=task)
        if form.is_valid():
            task.status = "ENTREGADA"                  # Cambiar estado
            task.delivery_date = timezone.now()        # Guardar fecha de entrega
            task.save()
            messages.success(request, "Tarea entregada correctamente.")
            return redirect("tasks:list_my_tasks")
    else:
        form = DeliverTaskForm(instance=task)

    return render(request, "tasks/deliver_task.html", {"form": form, "task": task})


# Cancelar entrega (alumno)
@login_required
def cancel_delivery(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    # Solo creador o miembros pueden cancelar
    if task.creator != request.user and not task.members.filter(id=request.user.id).exists():
        messages.error(request, "No tienes permisos para cancelar esta entrega.")
        return redirect("tasks:list_my_tasks")

    # Solo se puede cancelar si está entregada
    if task.status != "ENTREGADA":
        messages.warning(request, "La tarea no está en estado entregada.")
        return redirect("tasks:list_my_tasks")

    # Revertir estado y eliminar archivo
    task.status = "PENDIENTE"
    task.delivery_file.delete(save=False)
    task.delivery_date = None
    task.save()

    messages.success(request, "Entrega cancelada correctamente.")
    return redirect("tasks:list_my_tasks")


# Validar una tarea (profesor)
@login_required
def validate_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    # Solo profesores o admin pueden validar
    if request.user.role != "teacher" and not request.user.is_superuser:
        messages.error(request, "No tienes permisos para validar tareas.")
        return redirect("tasks:list_my_tasks")

    if not task.requires_teacher_validation:
        messages.error(request, 'Esta tarea no requiere validación del profesor.')
        return redirect("tasks:tasks_to_validate")

    if task.status != 'ENTREGADA':
        messages.warning(request, 'La tarea debe estar entregada para validarla.')
        return redirect("tasks:tasks_to_validate")

    task.status = 'VALIDADA'
    task.teacher_validator = request.user
    task.save()

    messages.success(request, 'Tarea validada correctamente.')
    return redirect("tasks:tasks_to_validate")


# Ver detalle de una tarea
@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    return render(request, 'tasks/task_detail.html', {'task': task})


# Validación por parte del alumno (cuando NO requiere profesor)
@login_required
def validate_task_by_student(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    # Solo si NO requiere profesor
    if task.requires_teacher_validation:
        messages.error(request, "Esta tarea requiere validación del profesor.")
        return redirect("tasks:detail", task_id=task.id)

    # Solo si está pendiente
    if task.status != "PENDIENTE":
        messages.warning(request, "La tarea ya no está pendiente.")
        return redirect("tasks:detail", task_id=task.id)

    task.status = "COMPLETADA"
    task.save()

    messages.success(request, "Has marcado la tarea como completada.")
    return redirect("tasks:detail", task_id=task.id)

