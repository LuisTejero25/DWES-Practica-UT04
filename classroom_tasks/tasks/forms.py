from django import forms
from .models import Task
from accounts.models import User


class IndividualTaskForm(forms.ModelForm):  # Formulario para tareas individuales
    class Meta:
        model = Task
        fields = [
            "title",                       # Título de la tarea
            "description",                 # Descripción
            "requires_teacher_validation", # Si necesita validación del profesor
            "due_date",                    # Fecha límite
        ]

    def save(self, commit=True):  # Guardado personalizado
        task = super().save(commit=False)
        task.type = "INDIVIDUAL"  # Tipo de tarea
        if commit:
            task.save()
        return task


class GroupTaskForm(forms.ModelForm):  # Formulario para tareas grupales
    members = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(role="ALUMNO"),  # Solo alumnos
        widget=forms.CheckboxSelectMultiple,          # Checkboxes
        required=True,                                # Obligatorio
        label="Miembros del grupo"                    # Etiqueta
    )

    class Meta:
        model = Task
        fields = [
            "title",                       # Título
            "description",                 # Descripción
            "members",                     # Miembros del grupo
            "requires_teacher_validation", # Validación del profesor
            "due_date",                    # Fecha límite
        ]

    def save(self, commit=True):  # Guardado personalizado
        task = super().save(commit=False)
        task.type = "GRUPAL"      # Tipo de tarea
        if commit:
            task.save()
            self.save_m2m()       # Guardar relación muchos a muchos
        return task


class TaskDeliveryForm(forms.ModelForm):  # Formulario para entregar archivo
    class Meta:
        model = Task
        fields = ["delivery_file"]  # Archivo de entrega
