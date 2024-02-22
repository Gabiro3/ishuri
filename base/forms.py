from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.contrib.auth.models import User
from django import forms

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
        fields = ['name', 'description', 'hour' , 'day']

class ClassesForm(ModelForm):
    class Meta:
        model = MyClasses
        fields = ['name', 'hour', 'description' ,  'school', 'day']

class ScheduleForm(ModelForm):
    class Meta:
        fields = ['title', 'time']

class WorkSpaceForm(ModelForm):
    class Meta:
        model = WorkSpace
        fields = ['title']

class NotesForm(ModelForm):
    class Meta:
        model = Notes
        fields = ['description', 'links']

class MarksForm(ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'grade']

