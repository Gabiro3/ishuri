from rest_framework import serializers
from base.models import Teacher, Assignment, Event, MyClasses, Schedule, Announcement, WorkSpace, Notes, Student, CustomUserManager
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['name', 'email', 'avatar', 'is_staff', 'is_active', 'password', 'password2']

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Passwords must match"})
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"],
            username=validated_data["name"],
            password=validated_data["password"]
        )
        user.is_staff = validated_data.get("is_staff", False)
        user.is_active = validated_data.get("is_active", True)
        user.avatar = validated_data.get("avatar", "avatar.svg")
        user.save()
        return user
class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'

class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class MyClassesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyClasses
        fields = '__all__'

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'

class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = '__all__'

class WorkSpaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkSpace
        fields = '__all__'

class NotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'