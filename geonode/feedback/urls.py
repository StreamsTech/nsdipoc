from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from views import UserFeedbackList, UserFeedbackCreate

urlpatterns = patterns(
    'geonode.feedback.views',

    # home page section management with image and texts
    url(r'^list$', UserFeedbackList.as_view(), name='user_feedback_list'),
    url(r'^create$', UserFeedbackCreate.as_view(), name='user_feedback_create'),
    # url(r'^slider-image/(?P<image_pk>[0-9]+)/(?P<section_pk>[0-9]+)/update$', SliderImageUpdate.as_view(),
    #     name='slider-image-update'),
    # url(r'^slider-image/(?P<image_pk>[0-9]+)/(?P<section_pk>[0-9]+)/delete$', SliderImageDelete.as_view(),
    #     name='slider-image-delete'),
    # # url(r'^slider-image/(?P<news_pk>[0-9]+)/details$', NewsDetails.as_view(), name='news-details'),

)
