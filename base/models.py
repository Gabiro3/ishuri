from django.db import models
# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, username, password, **extra_fields)

class Teacher(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=True)
    name = models.CharField(max_length=150, unique=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    avatar = models.ImageField(null=False, default='avatar.svg')
    is_dark = models.BooleanField(null=False, default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


#--- ASSIGNMENTS MODEL ---

class Assignment(models.Model):
    host = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200, null=True)
    description = models.TextField(null=True)
    assigned_class = models.IntegerField(null=True)
    submission_date = models.CharField(max_length=300, null=True)
    uploaded = models.DateTimeField(auto_now=True)
    submitted = models.CharField(max_length=50, default='False')

    class Meta:
        ordering = ['-uploaded']

    def __str__(self):
        return self.name
    

#--- EVENTS MODEL ---

class Event(models.Model):
    host = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200, null=True)
    description = models.TextField(null=False)
    hour = models.CharField(max_length=100, null=True)
    day = models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.name

#--- CLASSES MODEL ---

class MyClasses(models.Model):
    host = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200, null=False)
    description = models.CharField(max_length=300, null=True)
    hour = models.CharField(max_length=100, null=True)
    school = models.CharField(max_length=200, null=True)
    day = models.CharField(max_length=200, null=True)


#--Schedule Planner model ---


class Schedule(models.Model):
    host = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200)
    time = models.TimeField(null=True)

    def __str__(self):
        return self.name


# #-- Announcements model --

class Announcement(models.Model):

    title = models.CharField(max_length=200, null=True)
    description = models.TextField(null=True)
    uploaded = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-uploaded']

    def __str__(self):
        return self.title
    

class WorkSpace(models.Model):
    title = models.CharField(max_length=200, null=True)
    host = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)
    notes = models.ManyToManyField('Notes', related_name='related')

class Notes(models.Model):
    workspace = models.ForeignKey(WorkSpace, on_delete=models.CASCADE, null=True, related_name="workspace")
    description = models.CharField(max_length=500, null=True)
    links = models.CharField(max_length=200, null=True)


class Student(models.Model):
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    grade = models.IntegerField(null=True)
    assignments = models.ManyToManyField(Assignment, related_name='assignments')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)
