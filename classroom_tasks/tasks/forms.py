from django import forms
from .models import Task
from accounts.models import User


class IndividualTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            "title",
            "description",
            "requires_teacher_validation",
            "due_date",
        ]

    def save(self, commit=True):
        task = super().save(commit=False)
        task.type = "INDIVIDUAL"
        if commit:
            task.save()
        return task


class GroupTaskForm(forms.ModelForm):
    members = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(role="ALUMNO"),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Miembros del grupo"
    )

    class Meta:
        model = Task
        fields = [
            "title",
            "description",
            "members",
            "requires_teacher_validation",
            "due_date",
        ]

    def save(self, commit=True):
        task = super().save(commit=False)
        task.type = "GRUPAL"
        if commit:
            task.save()
            self.save_m2m()
        return task


class TaskDeliveryForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["delivery_file"]
