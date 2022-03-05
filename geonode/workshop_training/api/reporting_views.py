import logging

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.generics import ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet

from geonode.workshop_training.models import WorkshopTraining, WorkshopDocument
from geonode.workshop_training.api.serializers import WorkshopTrainingSerializer, WorkshopDocumentListSerializer

logger = logging.getLogger(__name__)


class ReportingAPICustomPagination(LimitOffsetPagination):
    default_limit = 10


class WorkshopTrainingListApiView(ModelViewSet):
    queryset = WorkshopTraining.objects.all().order_by("-date_created")

    def get_serializer_class(self):
        serializer_class = WorkshopTrainingSerializer
        return serializer_class



class WorkshopDocumentsListApiView(ModelViewSet):

    def get_queryset(self):
        workshop_id = self.kwargs['workshop_pk']
        return WorkshopTraining.objects.filter(id=workshop_id)

    def get_serializer_class(self):
        serializer_class = WorkshopDocumentListSerializer
        return serializer_class
