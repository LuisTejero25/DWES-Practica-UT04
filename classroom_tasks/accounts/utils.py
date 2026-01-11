# accounts/utils.py

def is_teacher(user):
    """
    Comprueba si el usuario es profesor o superusuario.
    Se usa en los decoradores @user_passes_test.
    """
    return user.is_authenticated and (user.role == "teacher" or user.is_superuser)
