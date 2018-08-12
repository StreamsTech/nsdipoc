
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.metadata import BaseMetadata

from geonode.rest_authentications import CsrfExemptSessionAuthentication
from rest_framework.response import Response
from rest_framework import status
from geonode.people.models import Profile
from serializers import UserSerializer



class MinimalMetadata(BaseMetadata):
    """
    Don't include field and other information for `OPTIONS` requests.
    Just return the name and description.
    """
    def determine_metadata(self, request, view):
        return {
            'name': view.get_view_name(),
            'description': view.get_view_description()
        }


class CommitteeList(ListAPIView):

    permission_classes = (IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication,)

    queryset = Profile.objects.filter(is_working_group_admin=True)
    serializer_class = UserSerializer
    metadata_class = MinimalMetadata
    # permission_classes = (IsAdminUser,)




