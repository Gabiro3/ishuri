from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from .models import *
from .forms import *
from datetime import datetime
import logging
logger = logging.getLogger(__name__)
def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('teacher')
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')

        try:
            user = Teacher.objects.get(email=name)
        except:
            messages.error(request, 'User does not exist')
        user = authenticate(request, email=name, password=password)
        if user is not None:
            login(request, user)
            logger.info(f"User {user.get_username()} - Logged In")
            return redirect('teacher')
        else:
            messages.error(request, 'Invalid Login credentials')
    context = {'page': page}

    return render(request, 'html/login_register.html', context)
    

def logoutUser(request):
    logout(request)
    return redirect('login')

def registerPage(request):
    form = TeacherCreationForm()
    if request.method == 'POST':
        form = TeacherCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = user.email.lower()
            user.save()
            login(request, user)
            return redirect('teacher')
        else:
            messages.error(request, 'An error occurred during registration!')
    return render(request, 'html/login_register.html', {'form': form})


@login_required(login_url='login')
def teacher(request):
    owner = Q(host = request.user)
    now = datetime.now()
    current_day = now.strftime("%A")
    current_date = now.strftime("%d")
    current_month = now.strftime("%B")
    current_time = Q(day=current_day)
    classes_today = MyClasses.objects.filter(owner & current_time)
    activities_today = Event.objects.filter(owner & current_time)
    assignments = Assignment.objects.filter(host=request.user)
    events = Event.objects.filter(host=request.user)
    announcements = Announcement.objects.all()
    classes = MyClasses.objects.all()
    context = {'assignments': assignments,
                'events': events,
                  'announcements': announcements
                  , 'classes': classes,
                    'classes_today': classes_today,
                      'activities_today': activities_today,
                      'date': current_date, 'month': current_month}
    return render(request, 'html/teacher-view.html', context)

@login_required(login_url='login')
def userProfile(request, pk):
    user = Teacher.objects.get(id=pk)
    announcements = Announcement.objects.all()
    context = {'user': user, 'announcements': announcements}
    return render(request, 'html/profile.html', context)

@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)
        else:
            messages.error(request, "Something wrong with the new data!")

    return render(request, 'html/update-user.html', {'form': form})

@login_required(login_url='login')
def createAssignment(request):
    form = AssignmentForm()

    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            assignement = form.save(commit=False)
            assignement.host = request.user
            assignement.save()
        return redirect('teacher')
    context = {'form': form}
    return render(request, 'html/assignment-form.html', context)

@login_required(login_url='login')
def deleteAssignment(request, pk):
    assignment = Assignment.objects.get(school_id=pk)
    if request.method == 'POST':
        assignment.delete()
        return redirect('teacher')
    return render(request, 'html/assignments-view.html', {'obj': assignment})

@login_required(login_url='login')
def createEvent(request):
    form = EventForm()

    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.host = request.user
            user.save()
        return redirect('teacher')
    context = {'form': form}
    return render(request, 'html/event-form.html', context)

@login_required(login_url='login')
def deleteEvent(request, pk):
    event = Event.objects.get(id=pk)
    if request.user != event.host:
        return HttpResponse("You don't have enough privileges to perform this action")
    if request.method == 'POST':
        event.delete()
        return redirect('teacher')
    
    return render(request, 'html/events-view.html', {'obj': event})

@login_required(login_url='login')
def createSchedule(request):
    form = ScheduleForm()

    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('teacher')
    context = {'form': form}
    return render(request, 'html/create-schedule.html', context)

@login_required(login_url='login')
def deleteSchedule(request, pk):
    schedule = Schedule.objects.get(id=pk)
    if request.user != schedule.host:
        return HttpResponse("You don't have enough privileges to perform this action")
    if request.method == 'POST':
        schedule.delete()
        return redirect('teacher')
    
    return render(request, 'html/schedule-view.html', {'obj': schedule})


@login_required(login_url='login')
def viewClasses(request):
    now = datetime.now()
    owner = Q(host=request.user)
    current_day = now.strftime("%A")
    current_time = Q(day=current_day)
    classes_today = MyClasses.objects.filter(owner & current_time)
    classes = MyClasses.objects.filter(host=request.user)
    events = Event.objects.filter(host=request.user)
    announcements = Announcement.objects.all()
    context = {'classes': classes, 'events': events, 'announcements': announcements, 'classes_today': classes_today}

    return render(request, 'html/classes-view.html', context)
@login_required(login_url='login')
def viewActivities(request):
    owner = Q(host=request.user)
    now = datetime.now()
    current_day = now.strftime("%A")
    current_time = Q(day=current_day)
    activities_today = Event.objects.filter(owner & current_time)
    activities = Event.objects.filter(host=request.user)
    events = Event.objects.all()
    announcements = Announcement.objects.all()
    context = {'events': events, 'announcements': announcements, 'activities_today': activities_today, 'activities': activities}

    return render(request, 'html/schedule-view.html', context)
@login_required(login_url='login')
def viewAssignments(request):
    assignments = Assignment.objects.filter(host=request.user)
    announcements = Announcement.objects.all()
    context = {'assignments': assignments, 'announcements': announcements,}

    return render(request, 'html/assignments-view.html', context)


@login_required(login_url='login')
def addClass(request):
    form = ClassesForm()
    if request.method == 'POST':
        form = ClassesForm(request.POST)
        if form.is_valid():
            classes = form.save(commit=False)
            classes.host = request.user
            classes.save()
        return redirect('classes-view')
    context = {'form': form}
    return render(request, 'html/add-class.html', context)






