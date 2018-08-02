# rest_framework api
import views

from django.conf.urls import url


urlpatterns = [
    url(r'^data-catalog/$', views.UserFeedbackCreateAPIView.as_view()),
]
