from django.contrib import messages  # Sistema de mensajes de Django
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from accounts.forms import CustomUserCreationForm
from accounts.models import User
from accounts.utils import is_teacher  # Tu función de comprobación de rol

@user_passes_test(is_teacher) 
def list_users_view(request): 
    users = User.objects.all() 
    return render(request, "accounts/list_users.html", {"users": users})


@login_required
def profile_view(request):  # Vista del perfil del usuario
    return render(request, "accounts/profile.html")  # Django ya pasa request.user por defecto


@user_passes_test(is_teacher)               # Solo profesores o admin pueden registrar usuarios
def register_user_view(request):            # Vista para registrar nuevos usuarios
    if request.method == "POST":            # Si el formulario fue enviado
        form = CustomUserCreationForm(request.POST)  # Cargamos los datos enviados

        if form.is_valid():                 # Validamos el formulario
            user = form.save(commit=False)  # Creamos el usuario sin guardar aún
            user.set_password(form.cleaned_data["password1"])  # Encriptamos la contraseña
            user.save()                     # Guardamos el nuevo usuario en la BD

            # Mensaje de éxito para el profesor
            messages.success(request, f"Usuario '{user.username}' creado correctamente.")

            return redirect("tasks:list_my_tasks")   # Volvemos al listado principal de tareas

        else:
            # Mensaje de error si el formulario no es válido
            messages.error(request, "Error al crear el usuario. Revisa los datos introducidos.")

    else:
        form = CustomUserCreationForm()     # Formulario vacío para GET

    # Renderizamos la plantilla con el formulario
    return render(request, "accounts/register.html", {"form": form})


