from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Mostrar campos adicionales en la lista de usuarios
    list_display = ("username", "email", "first_name", "last_name", "role", "is_staff", "is_superuser")
    list_filter = ("role", "is_staff", "is_superuser", "is_active")

    # Añadir el campo 'role' en el formulario de edición
    fieldsets = UserAdmin.fieldsets + (
        ("Rol", {"fields": ("role",)}),
    )

    # Añadir el campo 'role' en el formulario de creación
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Rol", {"fields": ("role",)}),
    )
