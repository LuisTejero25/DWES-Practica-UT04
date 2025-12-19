from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import TaskForm
from .models import Task

# Crear una nueva tarea (alumno/profesor)
@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.creator = request.user
            task.status = 'PENDIENTE'
            task.save()
            form.save_m2m()
            messages.success(request, 'Tarea creada correctamente.')
            return redirect("tasks:list_my_tasks")
    else:
        form = TaskForm()
    return render(request, 'tasks/create_task.html', {'form': form})


# Listar las tareas del usuario (creadas y en las que colabora)
@login_required
def list_my_tasks(request):
    created = Task.objects.filter(creator=request.user).distinct()
    collaborating = Task.objects.filter(members=request.user).exclude(creator=request.user).distinct()
    return render(
        request,
        'tasks/list_my_tasks.html',
        {'created': created, 'collaborating': collaborating}
    )


# Listar tareas que requieren validación del profesor
@login_required
def tasks_to_validate(request):
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

    if task.status != 'PENDIENTE':
        messages.warning(request, 'La tarea ya está entregada o validada.')
        return redirect("tasks:list_my_tasks")

    task.status = 'ENTREGADA'
    task.save()
    messages.success(request, 'Tarea entregada.')
    return redirect("tasks:list_my_tasks")


# Validar una tarea (profesor)
@login_required
def validate_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if not task.requires_teacher_validation:
        messages.error(request, 'Esta tarea no requiere validación de profesor.')
        return redirect("tasks:tasks_to_validate")

    if task.status != 'ENTREGADA':
        messages.warning(request, 'La tarea debe estar entregada para poder validarla.')
        return redirect("tasks:tasks_to_validate")

    task.status = 'VALIDADA'
    task.teacher_validator = request.user
    task.save()
    messages.success(request, 'Tarea validada.')
    return redirect("tasks:tasks_to_validate")

# Ver detalle de una tarea
@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    return render(request, 'tasks/task_detail.html', {'task': task})

