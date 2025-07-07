from django import forms
from tasks.models import Task
from users.models import CustomUser

class TaskAssignmentForm(forms.ModelForm):
    employee = forms.ModelChoiceField(queryset=CustomUser.objects.filter(role='EMP'))

    class Meta:
        model = Task
        fields = ['employee', 'title', 'description', 'due_date']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'})
        }

class UserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'role']
