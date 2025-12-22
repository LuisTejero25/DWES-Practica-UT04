from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'type', 'members', 
                  'requires_teacher_validation', 'due_date']

    def clean(self):
        cleaned_data = super().clean()
        task_type = cleaned_data.get('type')
        members = cleaned_data.get('members')

        if task_type == 'GRUPAL' and not members:
            raise forms.ValidationError("Las tareas grupales deben tener miembros asignados.")
        return cleaned_data

class TaskDeliveryForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["delivery_file"]
