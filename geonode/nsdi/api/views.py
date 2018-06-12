from rest_framework.views import APIView
from serializers import SectorSerializer
from rest_framework.response import Response
from rest_framework import generics

from geonode.nsdi.models import SectorModel


class SectorListAPI(generics.ListAPIView):
    queryset = SectorModel.objects.all()
    serializer_class = SectorSerializer

