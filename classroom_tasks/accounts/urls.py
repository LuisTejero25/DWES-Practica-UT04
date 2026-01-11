from django.urls import path  # Sistema de rutas
from . import views           # Importamos las vistas

app_name = "accounts"  # Namespace de la app

urlpatterns = [
    path("users/", views.list_users_view, name="list_users"),
    path("profile/", views.profile_view, name="profile"),         # Perfil del usuario autenticado
    path("register/", views.register_user_view, name="register"), # Registro de nuevos usuarios (solo profesor)
]
