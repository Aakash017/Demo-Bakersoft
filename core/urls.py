from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers
from core import views
router_v1 = routers.DefaultRouter()
router_v1.register(r'user', views.UserViewset, basename='user')
router_v1.register(r'project', views.ProjectsViewSet, basename='project')
router_v1.register(r'time_track', views.TimeTrackingView, basename='time_track')

urlpatterns = [
    url(r'', include(router_v1.urls)),
]
