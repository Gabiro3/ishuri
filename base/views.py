from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from .models import *
from .forms import *
from django.urls import reverse
from datetime import datetime
import logging
import statistics
from django.db.models import Avg
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
    message = "Welcome to Ishuri Bridge"
    current_day = now.strftime("%A")
    current_date = now.strftime("%d")
    current_month = now.strftime("%B")
    current_time = Q(day=current_day)
    classes_today = MyClasses.objects.filter(owner & current_time)
    activities_today = Event.objects.filter(owner & current_time)
    assignments = Assignment.objects.filter(host=request.user)
    activities = Event.objects.get(host = request.user)
    events = Event.objects.filter(host=request.user)
    announcements = Announcement.objects.all()
    classes = MyClasses.objects.all()
    user_theme = request.user.is_dark
    context = {'assignments': assignments,
               'theme': user_theme,
                'events': events,
                  'announcements': announcements
                  , 'classes': classes,
                    'classes_today': classes_today,
                      'activities_today': activities_today,
                      'activities': activities,
                      'date': current_date, 'month': current_month, 'message': message}
    return render(request, 'html/teacher-view.html', context)

@login_required(login_url='login')
def userProfile(request, pk):
    message = request.GET.get('message')
    user = Teacher.objects.get(id=pk)
    announcements = Announcement.objects.all()
    context = {'user': user, 'announcements': announcements, 'message': message}
    return render(request, 'html/profile.html', context)

@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            message = "Profile updated successfully"
            user_id = user.id
# Redirect with message included as a query parameter

            form.save()
            return redirect(reverse('user-profile', kwargs={'pk': user_id}) + '?message=' + message)
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
            message = "Assignment created successfully"
        return redirect(reverse('view-assignments') + '?message=' + message)
    context = {'form': form}
    return render(request, 'html/assignment-form.html', context)

@login_required(login_url='login')
def deleteAssignment(request, pk):
    assignment = Assignment.objects.get(id=pk)
    assignment.delete()
    return redirect('view-assignments')

@login_required(login_url='login')
def createEvent(request):
    form = EventForm()

    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.host = request.user
            user.save()
            message = "Activity created successfully"
        return redirect(reverse('view-activities') + '?message=' + message)
    context = {'form': form}
    return render(request, 'html/event-form.html', context)

@login_required(login_url='login')
def deleteEvent(request, pk):
    event = Event.objects.get(id=pk)
    if request.user != event.host:
        return HttpResponse("You don't have enough privileges to perform this action")
    event.delete()
    return redirect('view-activities')

@login_required(login_url='login')
def createSchedule(request):
    form = ScheduleForm()

    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        if form.is_valid():
            form.save()
            message = "Activity created successfully"
        return redirect(reverse('view-activities') + '?message=' + message)
    context = {'form': form}
    return render(request, 'html/create-schedule.html', context)

@login_required(login_url='login')
def deleteSchedule(request, pk):
    schedule = Schedule.objects.get(id=pk)
    if request.user != schedule.host:
        return HttpResponse("You don't have enough privileges to perform this action")
    if request.method == 'POST':
        schedule.delete()
        message = "Activity deleted successfully"
        return redirect(reverse('view-activities') + '?message=' + message)
    
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
def updateActivity(request, pk):
    event = Event.objects.get(id=pk)
    form = EventForm(instance=event)

    if request.method == 'POST':
        form = EventForm(request.POST,instance=event)
        if form.is_valid():
            form.save()
            message = "Activity updated successfully"
            return redirect(reverse('view-activities') + '?message=' + message)
        else:
            messages.error(request, "Something wrong with the new data!")

    return render(request, 'html/update-user.html', {'form': form})
@login_required(login_url='login')
def viewAssignments(request):
    assignments = Assignment.objects.filter(host=request.user)
    announcements = Announcement.objects.all()
    context = {'assignments': assignments, 'announcements': announcements,}

    return render(request, 'html/assignments-view.html', context)
@login_required(login_url='login')
def updateAssignment(request, pk):
    assignment = Assignment.objects.get(id=pk)
    form = AssignmentForm(instance=assignment)

    if request.method == 'POST':
        form = AssignmentForm(request.POST,instance=assignment)
        if form.is_valid():
            form.save()
            message = "Assignment updated successfully"
            return redirect(reverse('view-assignments') + '?message=' + message)
        else:
            messages.error(request, "Something wrong with the new data!")

    return render(request, 'html/update-user.html', {'form': form})


@login_required(login_url='login')
def addClass(request):
    form = ClassesForm()
    if request.method == 'POST':
        form = ClassesForm(request.POST)
        if form.is_valid():
            classes = form.save(commit=False)
            classes.host = request.user
            message = "Class created successfully"
        return redirect(reverse('classes-view') + '?message=' + message)
    context = {'form': form}
    return render(request, 'html/add-class.html', context)

@login_required(login_url='login')
def updateClass(request, pk):
    class_instance = MyClasses.objects.get(id=pk)
    form = ClassesForm(instance=class_instance)

    if request.method == 'POST':
        form = ClassesForm(request.POST,instance=class_instance)
        if form.is_valid():
            form.save()
            message = "Class updated successfully"
            return redirect(reverse('classes-view') + '?message=' + message)
        else:
            messages.error(request, "Something wrong with the new data!")

    return render(request, 'html/update-user.html', {'form': form})

@login_required(login_url='login')
def deleteClass(request, pk):
    assignment = MyClasses.objects.get(id=pk)
    assignment.delete()
    return redirect('classes-view')

@login_required(login_url='login')
def workSpace(request):
    workspaces = WorkSpace.objects.all()
    notes = Notes.objects.all()
    context = {'workspaces': workspaces, 'files':notes}
    return render(request, 'html/workspace-home.html', context)

@login_required(login_url='login')
def workSpaceView(request, name):
    workspace = WorkSpace.objects.get(title=name)
    notes = Notes.objects.filter(workspace=workspace.id)
    context = {'notes': notes, 'name': name}
    return render(request, 'html/view-workspace.html', context)

@login_required(login_url='login')
def createWorkSpace(request):
    if request.method == 'POST':
        form = WorkSpaceForm(request.POST)
        name = request.POST.get('title')

        if form.is_valid():
            workspace = form.save()
            message = "Workspace created successfully"
            return redirect(reverse('workspace') + '?message=' + message)
        else:
            messages.error(request, "Something wrong with the new data!")
    else:
        form = WorkSpaceForm()

    context = {'form': form}
    return render(request, 'html/create-workspace.html', context)

@login_required(login_url='login')
def addNote(request, name):
    try:
        workspace = WorkSpace.objects.get(title=name)
    except WorkSpace.DoesNotExist:
        # Handle the case where the workspace with the given title doesn't exist
        message = "Workspace not found"
        return redirect(reverse('workspace') + '?message=' + message)

    form = NotesForm()

    if request.method == 'POST':
        form = NotesForm(request.POST)

        if form.is_valid():
            # Create a new note object but don't save it to the database yet
            note = form.save(commit=False)
            note.workspace = workspace
            note.save()

            # Assuming you want to associate notes with the workspace using a ManyToManyField
            workspace.notes.add(note)

            message = "Note added successfully"
            return redirect(reverse('view-work', name=name) + '?message=' + message)
        else:
            # Display form validation errors
            messages.error(request, "Invalid Input Data")

    context = {'workspace': workspace, 'form': form}
    return render(request, 'html/add-notes.html', context)


@login_required(login_url='login')
def deleteWorkSpace(request, pk):
    workspace = WorkSpace.objects.get(id=pk)
    workspace.delete()
    message = "Workspace deleted successfully"
    return redirect(reverse('workspace') + '?message=' + message)

@login_required(login_url='login')
def Announcements(request):
    return render(request, 'html/announcements-view.html')


@login_required(login_url='login')
def CreateMarks(request):
    form = MarksForm()
    assignment = Assignment.objects.get(name="Assign Test")
    if request.method == "POST":
        form = MarksForm(request.POST)
        if form.is_valid():
            marks = form.save(commit=False)
            marks.save()
            marks.assignments.set([assignment])
            message = "Student Marks created successfully"
            return redirect(reverse('marks', kwargs={'name': assignment.name}) + '?message=' + message)
        else:
            return messages.error('Record could not be added! check again the inputs')
    return render(request, 'html/add-marks.html', {'form': form})

@login_required(login_url='login')
def viewMarks(request, name):
    marks = Student.objects.filter(teacher=request.user)
    students = Student.objects.all()
    average_grade = 0
    assignments = Assignment.objects.filter(host=request.user)
    for assignment in assignments:
        students = Student.objects.filter(assignments__id=assignment.id)
        average_grade = Student.objects.aggregate(avg_grade=Avg('grade'))['avg_grade']
    context = {'marks': marks, 'average': average_grade, 'assignments': assignments, 'students': students}
    return render(request, 'html/view-marks.html', context)


@login_required(login_url='login')
def viewStudents(request, pk):
    assignment = Assignment.objects.get(id=pk)
    students = Student.objects.filter(assignments__id=pk)
    average = 20
    context = {'students': students, 'average': average, 'assignment':assignment}
    return render(request, 'html/view-students.html', context)

@login_required(login_url='login')
def updateMarks(request, pk):
    marks = Student.objects.get(id=pk)
    if marks.teacher != request.user:
        return HttpResponse("You don't have enough privileges to access this data!")
    form = MarksForm(instance=marks)
    if request.method == 'POST':
        form = MarksForm(request.user)
        if form.is_valid():
            form = MarksForm(request.POST, instance=marks)
            message = "Marks updated successfully"
            marks = form.save(commit=False)
            name = marks.assignments
            assignment = Assignment.objects.get(id=name)
# Redirect with message included as a query parameter

            form.save()
            return redirect(reverse('view-students', kwargs={'pk': assignment.id}) + '?message=' + message)
    

@login_required(login_url='login')
def deleteMarks(request, pk):
    marks = Student.objects.get(id=pk)
    if marks.teacher != request.user:
        return HttpResponse("User not allowed for this action")
    pk = Student.objects.filter(assignment__Id=pk)
    marks.delete()
    message = "Student Marks deleted successfully!"
    return redirect(reverse('view-students', kwargs={'pk': pk}) + '?message=' + message)




