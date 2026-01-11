"""
URL configuration for classroom_tasks project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),                       # Panel de administración

    path('tasks/', include('tasks.urls')),                 # Rutas de la app de tareas
 
    # Logout que acepta GET y redirige al login 
    path( "accounts/logout/", auth_views.LogoutView.as_view(next_page="/accounts/login/"),
    name="logout" ),
    
    path('accounts/', include('django.contrib.auth.urls')),# Login, logout, password reset...
    path('accounts/', include('accounts.urls')),           # Rutas personalizadas de usuarios
   
]

