from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "tasks"

urlpatterns = [
    path('create/', views.create_task, name='create_task'),
    path('mine/', views.list_my_tasks, name='list_my_tasks'),
    path('to-validate/', views.tasks_to_validate, name='tasks_to_validate'),
    path('<int:task_id>/deliver/', views.deliver_task, name='deliver_task'),
    path('<int:task_id>/validate/', views.validate_task, name='validate_task'),
    path('<int:task_id>/', views.task_detail, name='detail'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('<int:task_id>/cancel/', views.cancel_delivery, name='cancel_delivery'),


]

