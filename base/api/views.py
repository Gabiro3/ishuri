from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import Teacher, Assignment, Event, MyClasses, Announcement, WorkSpace, Notes, Student
from .serializers import TeacherSerializer, AssignmentSerializer, EventSerializer, MyClassesSerializer, AnnouncementSerializer, WorkSpaceSerializer, NotesSerializer, StudentSerializer

@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/rooms',
        'GET /api/rooms/:id'
    ]
    return Response(routes)



class TeacherListAPIView(APIView):
    def get(self, request):
        teachers = Teacher.objects.all()
        serializer = TeacherSerializer(teachers, many=True)
        return Response(serializer.data)

class TeacherDetailAPIView(APIView):
    def get(self, request, pk):
        try:
            teacher = Teacher.objects.get(id=pk)
            serializer = TeacherSerializer(teacher)
            return Response(serializer.data)
        except Teacher.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class AssignmentListAPIView(APIView):
    def get(self, request):
        assignments = Assignment.objects.all()
        serializer = AssignmentSerializer(assignments, many=True)
        return Response(serializer.data)

class AssignmentDetailAPIView(APIView):
    def get(self, request, pk):
        try:
            assignment = Assignment.objects.get(id=pk)
            serializer = AssignmentSerializer(assignment)
            return Response(serializer.data)
        except Assignment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

# Similarly, create APIViews for other models like Event, MyClasses, Announcement, WorkSpace, Notes, Student
