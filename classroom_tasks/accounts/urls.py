from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("profile/", views.profile_view, name="profile"),
    path("users/", views.users_list_view, name="users_list"),
]
