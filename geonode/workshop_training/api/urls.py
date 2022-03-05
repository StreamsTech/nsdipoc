from django.conf.urls import url

from reporting_views import WorkshopTrainingListApiView, WorkshopDocumentsListApiView


urlpatterns = [
    url(r'^workshop-list', WorkshopTrainingListApiView.as_view({'get': 'list'})),
    url(r'^workshop/(?P<workshop_pk>[0-9]+)/documents', WorkshopDocumentsListApiView.as_view({'get': 'list'})),

]
