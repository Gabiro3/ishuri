from django.urls import path
from . import views

urlpatterns = [
    path('',  views.getRoutes),
    path('teachers/', views.getTeachers),
    path('teacher/<str:pk>/', views.getTeacher),
    path('assignments/', views.getAssignments),
    path('events/', views.getEvents),
    path('classes/', views.getClasses),
    path('activities/', views.getActivities),
    path('announcements/', views.getAnnouncements),
    path('workspaces/', views.getWorkSpaces),
]