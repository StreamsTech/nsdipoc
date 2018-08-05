from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from views import UserFeedbackList, UserFeedbackCreate, UserFeedbackDetails, UserFeedbackDelete

urlpatterns = patterns(
    'geonode.feedback.views',

    # home page section management with image and texts
    url(r'^list$', UserFeedbackList.as_view(), name='user_feedback_list'),
    url(r'^create$', UserFeedbackCreate.as_view(), name='user_feedback_create'),

    url(r'^(?P<feedback_pk>[0-9]+)/delete$', UserFeedbackDelete.as_view(), name='user_feedback_delete'),
    url(r'^(?P<feedback_pk>[0-9]+)/details$', UserFeedbackDetails.as_view(), name='user_feedback_details'),
)
