from django.conf.urls import url

from views import ModelDataUploadFormOptionsAPIView, ModelDataUploadStatusAPIView
from views import UploadErrorDetailsAPIView, DataUploadFromFileAPIView, DmaZoneAPIView, BulkDmaUploadAPIView
from views import UacUploadAPIView, CommercialLossUploadAPIView
from views import DmaBulkMeterDeleteAPIView

from reporting_views import DPSListApiView
from scada_views import ScadaStatusAPIView

urlpatterns = [
    url(r'^data/upload', DataUploadFromFileAPIView.as_view()),
    url(r'^data/status/update', ModelDataUploadStatusAPIView.as_view()),
    url(r'^data/form/options', ModelDataUploadFormOptionsAPIView.as_view()),
    url(r'^data/error/(?P<pk>[0-9]+)/details', UploadErrorDetailsAPIView.as_view()),
    url(r'^data/dma-zone', DmaZoneAPIView.as_view()),
    url(r'^data/bulk-dma-upload', BulkDmaUploadAPIView.as_view()),
    url(r'^data/uac-upload', UacUploadAPIView.as_view()),
    url(r'^data/cl-upload', CommercialLossUploadAPIView.as_view()),

    #reporting api
    url(r'^dps-list', DPSListApiView.as_view()),

]
