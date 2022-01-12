from django.conf.urls import url

from reporting_views import DPSListApiView

urlpatterns = [
    url(r'^dps-list', DPSListApiView.as_view({'get': 'list'})),

]
