import logging

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.generics import ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet

from geonode.standardization.models import DataProductSpecification
from geonode.standardization.api.serializers import DPSSerializer

logger = logging.getLogger(__name__)


class ReportingAPICustomPagination(LimitOffsetPagination):
    default_limit = 10


class DPSListApiView(ModelViewSet):
    queryset = DataProductSpecification.objects.all()
    pagination_class = ReportingAPICustomPagination
    ordering_fields = ['title', 'document_type__name', 'organization__title', 'creation_date']
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['id', 'title', 'document_type__name', 'organization__title', 'creation_date']
    search_fields = ['title', 'document_type__name', 'organization__title', 'creation_date']

    def get_serializer_class(self):
        serializer_class = DPSSerializer
        return serializer_class
