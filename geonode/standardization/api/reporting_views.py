import logging

from rest_framework.generics import ListAPIView
from rest_framework.pagination import LimitOffsetPagination

from geonode.standardization.models import DataProductSpecification
from geonode.standardization.api.serializers import DPSSerializer

DPS_LIST_TABLE_HEADERS = ["Organization", "Type of Document", "Title", "Creation Date", "Action"]

logger = logging.getLogger(__name__)


class ReportingAPICustomPagination(LimitOffsetPagination):
    default_limit = 10


class DPSListApiView(ListAPIView):
    pagination_class = ReportingAPICustomPagination

    @staticmethod
    def get_query_string(query_params):
        query_dict = {}
        if 'zone_id' in query_params:
            query_dict['zone_id'] = query_params.get('zone_id', None)
        if 'dma_id' in query_params:
            query_dict['dma_id'] = query_params.get('dma_id', None)
        if 'year_month' in query_params:
            query_dict['year_month'] = query_params.get('year_month', None)
        if 'account_id' in query_params:
            query_dict['account_id__icontains'] = query_params.get('account_id', None)
        return query_dict

    def get_queryset(self):
        query_string = self.get_query_string(self.request.query_params)
        # queryset = model.objects.filter(**query_string).order_by('-date_created')
        queryset = DataProductSpecification.objects.all().order_by('-date_created')
        return queryset

    def get_serializer_class(self):
        serializer_class = DPSSerializer
        return serializer_class

    def list(self, request, *args, **kwargs):
        response = super(DPSListApiView, self).list(request, args, kwargs)
        response.data['report_table_headers'] = DPS_LIST_TABLE_HEADERS
        return response
