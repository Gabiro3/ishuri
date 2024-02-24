from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import *
from .serializers import *
from django.http import JsonResponse
import json
@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/teachers',
        'GET /api/teacher/:id',
        'GET /api/assignments',
        'GET /api/activities',
    ]
    return Response(routes)



@api_view(['GET'])
def getTeachers(request):
    teachers = Teacher.objects.all()
    serializer = TeacherSerializer(teachers, many=True)
    return Response(serializer.data)
@api_view(['GET'])
def getTeacher(request, pk):
    teachers = Teacher.objects.get(id=pk)
    serializer = TeacherSerializer(teachers)
    return Response(serializer.data)

@api_view(['GET'])
def getAssignments(request):
    assignments = Assignment.objects.all()
    serializer = AssignmentSerializer(assignments, many=True)
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def getAssignment(request, pk):
    assignment = Assignment.objects.get(id=pk)
    serializer = AssignmentSerializer(assignment)
    return JsonResponse(serializer.data, safe=False)

# Similarly, create APIViews for other models like Event, MyClasses, Announcement, WorkSpace, Notes, Student
@api_view(['GET'])
def getEvents(request):
    events = Event.objects.all()
    serializer = EventSerializer(events, many=True)
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def getClasses(request):
    classes = MyClasses.objects.all()
    serializer = MyClassesSerializer(classes, many=True)
    return JsonResponse(serializer.data, safe=False)
        

@api_view(['GET'])
def getActivities(request):
    activities = Schedule.objects.all()
    serializer = ScheduleSerializer(activities, many=True)
    return JsonResponse(serializer.data, safe=False)
        
@api_view(['GET'])
def getAnnouncements(request):
    announcements = Announcement.objects.all()
    serializer = AnnouncementSerializer(announcements, many=True)
    return JsonResponse(serializer.data, safe=False)



@api_view(['GET'])
def getWorkSpaces(request):
    workspaces = WorkSpace.objects.all()
    serializer = WorkSpaceSerializer(workspaces, many=True)
    return JsonResponse(serializer.data, safe=False)

