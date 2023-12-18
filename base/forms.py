from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.contrib.auth.models import User

class TeacherCreationForm(UserCreationForm):
    class Meta:
        model = Teacher
        fields = ['name', 'email', 'password1', 'password2']

class UserForm(ModelForm):
    class Meta:
        model = Teacher
        fields = ['name', 'email', 'avatar']

class AssignmentForm(ModelForm):
    class Meta:
        model = Assignment
        fields = ['name', 'description', 'assigned_class', 'submission_date']

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'day']

class ClassesForm(ModelForm):
    class Meta:
        model = MyClasses
        fields = ['name', 'hour', 'school', 'day']

class ScheduleForm(ModelForm):
    class Meta:
        fields = ['title', 'time']

