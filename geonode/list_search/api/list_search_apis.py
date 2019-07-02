# 23june2019
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from guardian.shortcuts import get_objects_for_user
from url_filter.integrations.drf import DjangoFilterBackend

from geonode.rest_authentications import CsrfExemptSessionAuthentication
from geonode.base.models import ResourceBase
from list_search_serializers import ResourceBaseListSearchSerializer


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 21
    page_size_query_param = 'page_size'
    max_page_size = 1000


class ResourceBaseListSearchAPIView(generics.ListAPIView):
    """
    This api is designed in DRF
    and this list api returns list of ACTIVE
    layers permitted for an user.
    This also supports filtering.
    such as: http://localhost:8000/api/list_search/layers-list?title=jjhhj
    here the api is called with a query string for the title field.
    """
    serializer_class = ResourceBaseListSearchSerializer
    # permission_classes = (IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication,)
    filter_backends = (DjangoFilterBackend,)
    pagination_class = LargeResultsSetPagination
    filter_fields = ["group", "category", "featured", "title", "tkeywords", "regions", "owner", "date",
                     "resource_type"]

    def get_queryset(self):
        permitted_ids = get_objects_for_user(
            self.request.user, 'base.view_resourcebase').values('id')
        order_by = self.request.query_params.get('order_by', None)
        queryset = ResourceBase.objects.distinct().filter(status='ACTIVE').filter(id__in=permitted_ids)
        if order_by is not None:
            queryset = queryset.order_by(order_by)
        return queryset
