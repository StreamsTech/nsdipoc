# rest_framework api
import views

from django.conf.urls import patterns, url
from geonode.analytics.enum import ContentTypeEnum


urlpatterns = [
    url(r'^non-gis/$', views.NonGISActivityCreateAPIView.as_view()),    
    url(r'^gis/$', views.GISActivityCreateAPIView.as_view()),
    url(r'^map/load/$', views.LoadActivityCreateAPIView.as_view(), {'content_type': ContentTypeEnum.MAP }),
]
