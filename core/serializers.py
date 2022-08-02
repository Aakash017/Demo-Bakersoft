from datetime import datetime

from rest_framework import serializers
from core.models import Project, TimeTracking


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class TimeTrackingSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source='user.email')
    project_title = serializers.CharField(source='project.title')

    class Meta:
        model = TimeTracking
        fields = ('user_email', 'project_title', 'login_time', 'logout_time',)

    def to_representation(self, instance):
        data = super(TimeTrackingSerializer, self).to_representation(instance)
        print(data)
        total_time = datetime.strptime(data.get("login_time"), '%Y-%m-%dT%H:%M:%S.%fZ') - datetime.strptime(
            data.get("logout_time"), '%Y-%m-%dT%H:%M:%S.%fZ')
        data["time_spent_in_seconds"] = total_time.seconds
        return data
