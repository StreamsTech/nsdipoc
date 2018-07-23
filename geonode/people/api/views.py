
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated

from geonode.rest_authentications import CsrfExemptSessionAuthentication
from rest_framework.response import Response
from rest_framework import status
from geonode.people.models import Profile
from serializers import UserSerializer



class CommitteeList(ListAPIView):

    permission_classes = (IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication,)

    queryset = Profile.objects.filter(is_working_group_admin=True)
    serializer_class = UserSerializer
    # permission_classes = (IsAdminUser,)



