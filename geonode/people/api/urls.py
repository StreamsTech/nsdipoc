# rest_framework api
import views

from django.conf.urls import url


urlpatterns =[
    url(r'^committee$', views.CommitteeList.as_view()),
]
