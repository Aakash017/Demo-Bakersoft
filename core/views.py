import datetime

from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404

# Create your views here.
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from core.models import User, Project, TimeTracking
from core.serializers import ProjectSerializer, TimeTrackingSerializer


class UserViewset(viewsets.ViewSet):
    permission_classes = (AllowAny,)

    @action(methods=['post'], detail=False, url_path="signup")
    def signup(self, request):
        try:
            data = request.data
            email = data.get("email").lower()
            pwd = data.get("password")
            u, is_created = User.objects.get_or_create(email=email)
            u.set_password(pwd)
            u.save()
            return Response({"data": f"User {email} created successfully"}, status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": f"got exception while create user {e}"}, status.HTTP_201_CREATED)

    @action(methods=['post'], detail=False, url_path="login")
    def login(self, request):
        try:
            data = request.data
            email = data.get("email").lower()
            pwd = data.get("password")
            proj = data.get("project")
            if not proj:
                return Response({"data": {"error": "project missing"}}, status=status.HTTP_400_BAD_REQUEST)
            proj = Project.objects.get(slug=proj)
            user = authenticate(username=email, password=pwd)
            if user is not None:
                if TimeTracking.objects.filter(user=user, project=proj, logout_time=None).exists():
                    return Response({"data": f"user {email} is already logged in {proj}"}, status=status.HTTP_200_OK)
                else:
                    TimeTracking.objects.create(user=user, project=proj, login_time=datetime.datetime.now())
                    return Response({"data": {"email": user.email,
                                              "message": "login successfully"}}, status.HTTP_200_OK)
            else:
                return Response({"data": "username or password not correct"}, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"data": f"exception while login {e}"}, status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False, url_path="logout")
    def logout(self, request):
        try:
            data = request.data
            email = data.get("email").lower()
            proj = data.get("project")
            if not proj or not email:
                return Response({"data": {"error": "email or proj missing"}}, status=status.HTTP_400_BAD_REQUEST)
            proj = Project.objects.get(slug=proj)
            user = User.objects.get(email=email)
            time_track = TimeTracking.objects.filter(user=user, project=proj, logout_time=None)
            if time_track:
                time_track = time_track[0]
                time_track.logout_time = datetime.datetime.now()
                time_track.save()
                return Response({"data": "logged out"}, status=status.HTTP_200_OK)
            else:
                return Response({"data": f"user {email} not logged in {proj}"}, status=status.HTTP_200_OK)

        except  Exception as e:
            return Response({"data": f"exception while logout {e}"}, status.HTTP_400_BAD_REQUEST)


class ProjectsViewSet(viewsets.ViewSet):
    permission_classes = (AllowAny,)

    def list(self, request):
        queryset = Project.objects.all()
        serializer = ProjectSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Project.objects.all()
        project = get_object_or_404(queryset, pk=pk)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path="create")
    def perform_create(self, request):
        data = request.data
        # project = Project(data)
        serializer = ProjectSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    @action(detail=False, methods=['patch'], url_path="update")
    def perform_update(self, request, pk=None):
        data = request.data
        pk = data.get("id")
        # project = Project(data)
        proj = get_object_or_404(Project, pk=pk)
        if proj:
            serializer = ProjectSerializer(proj, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class TimeTrackingView(viewsets.ViewSet):
    @action(detail=False, methods=['post'], url_path="fetch_all")
    def fetch_all(self, request):
        _filter = {}
        data = request.data
        filter_mapped_keys = {"login_time": "login_time__gte", "logout_time": "logout_time__gte",
                              "user_email": "user__email", "project_title": "project__title"}
        for key, val in data.items():
            _filter[filter_mapped_keys[key]] = val
        time_track = TimeTracking.objects.filter(**_filter)
        serializer = TimeTrackingSerializer(time_track, many=True)
        return Response(serializer.data)
