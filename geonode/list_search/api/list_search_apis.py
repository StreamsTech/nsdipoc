# 23june2019
from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from guardian.shortcuts import get_objects_for_user
from url_filter.integrations.drf import DjangoFilterBackend

from geonode.rest_authentications import CsrfExemptSessionAuthentication
from geonode.layers.models import Layer
from list_search_serializers import LayersListSearchSerializer


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 1000


class LayersListSearchAPIView(generics.ListAPIView):
    """
    This api is designed in DRF
    and this list api returns list of ACTIVE
    layers permitted for an user.
    This also supports filtering.
    such as: http://localhost:8000/api/list_search/layers-list?title=jjhhj
    here the api is called with a query string for the title field.
    """
    serializer_class = LayersListSearchSerializer
    # permission_classes = (IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication,)
    filter_backends = (DjangoFilterBackend,)
    pagination_class = LargeResultsSetPagination
    filter_fields = ["group", "category", "featured", "title", "tkeywords", "regions", "category", "owner", "date",
                     "resource_type", "geometry_type"]

    def get_queryset(self):
        permitted_ids = get_objects_for_user(
            self.request.user, 'base.view_resourcebase').values('id')
        queryset = Layer.objects.distinct().order_by('-date').filter(status='ACTIVE')
        return queryset.filter(id__in=permitted_ids)
