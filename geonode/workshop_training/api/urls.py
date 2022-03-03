from django.conf.urls import url

from reporting_views import WorkshopTrainingListApiView

urlpatterns = [
    url(r'^workshop-list', WorkshopTrainingListApiView.as_view({'get': 'list'})),

]
