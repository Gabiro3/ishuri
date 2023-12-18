from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.registerPage, name="register"),
    path('', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),

    path('teacher/', views.teacher, name="teacher"),

    path('profile/<str:pk>', views.userProfile, name="user-profile"),
    path('update-user/', views.updateUser, name="update-user"),

    path('add-assignment/', views.createAssignment, name="add-assignment"),
    path('delete-assignment/<str:pk>/', views.deleteAssignment, name="delete-assignment"),
    path('assignments/', views.viewAssignments, name="view-assignments"),

    path('add-event/', views.createEvent, name="create-event"),
    path('delete-event/<str:pk>/', views.deleteEvent, name="delete-event"),
    path('activities/', views.viewActivities, name="view-activities"),

    path('add-schedule/', views.createSchedule, name="create-schedule"),
    path('delete-schedule/<str:pk>/', views.deleteSchedule, name="delete-schedule"),

    path('add-class/', views.addClass, name="add-class"),
    path('delete-schedule/<str:pk>/', views.deleteSchedule, name="delete-class"),
    path('classes/', views.viewClasses, name="classes-view"),
]