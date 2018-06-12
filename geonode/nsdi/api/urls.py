# rest_framework api
import views

from django.conf.urls import url


urlpatterns =[
    url(r'^sectors$', views.SectorListAPI.as_view()),
]
