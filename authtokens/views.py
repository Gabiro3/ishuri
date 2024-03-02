from rest_framework import generics
from django.contrib.auth import get_user_model
from rest_framework import permissions, status
from rest_framework.response import Response
from .serializers import UserRegisterSerializer
from base.models import Teacher, Assignment, Event, MyClasses, Schedule, Announcement, WorkSpace, Notes, Student, CustomUserManager

class CustomUserRegisterView(generics.CreateAPIView):

    model = get_user_model()
    serializer_class = UserRegisterSerializer
    permission_classes = [
        permissions.AllowAny,
    ]

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        serializer = self.get_serializer(data=request.data)
        username = ""
        if serializer.is_valid():
           username = serializer.validated_data.get('email')

        # Return the response with the username and HTTP status code
        return Response({'username': username}, status=status.HTTP_201_CREATED)
