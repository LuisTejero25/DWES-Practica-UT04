from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from accounts.models import User


@login_required
def profile_view(request):
    return render(request, "accounts/profile.html", {"user": request.user})


@login_required
def list_users_view(request):
    users = User.objects.all().order_by("username")
    return render(request, "accounts/list_users.html", {"users": users})
