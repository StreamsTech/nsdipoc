from django.db.models import Count
from django.contrib.contenttypes.models import ContentType
from geonode.analytics.enum import ContentTypeEnum
from geonode.analytics.models import MapLoad,Visitor,LayerLoad,PinpointUserActivity, LoadActivity

from geonode.layers.models import Layer
from geonode.maps.models import Map
from geonode.documents.models import Document

from geonode.analytics.api.serializers import (
    MapLoadSerializer,
    LayerLoadSerializer,
    VisitorSerializer,
    PinpointUserActivitySerializer
)

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from rest_framework_gis.filters import InBBoxFilter

from geonode.analytics.mixin import AnalyticsMixin
# Create your views here.


class MapLoadListAPIView(ListAPIView):
    queryset = MapLoad.objects.all()
    serializer_class = MapLoadSerializer

    # set permission for admin


class LayerLoadListAPIView(ListAPIView):
    queryset = LayerLoad.objects.all()
    serializer_class = LayerLoadSerializer

    # set permission for admin


class VisitorListAPIView(ListAPIView):
    queryset = Visitor.objects.all()
    serializer_class = VisitorSerializer

    # set permission for admin


class PinpointUserActivityListAPIView(ListAPIView):
    queryset = PinpointUserActivity.objects.select_related().all()
    serializer_class = PinpointUserActivitySerializer
    bbox_filter_field = 'point'
    filter_backends = (InBBoxFilter,)

    # set permission for admin


class PinpointUserActivityCreateAPIView(APIView):

    def post(self, request, format=None):
        data = request.data

        pinpoint_user_activity = PinpointUserActivity()
        pinpoint_user_activity.user = None if request.user.id is None else request.user
        pinpoint_user_activity.map = None if str(data['map']) == '' else Map.objects.get(id=int(data['map']))
        pinpoint_user_activity.layer = None if str(data['layer']) == '' else Layer.objects.get(id=int(data['layer']))
        pinpoint_user_activity.ip = str(request.environ['REMOTE_ADDR'])
        pinpoint_user_activity.agent = str(request.environ['HTTP_USER_AGENT'])
        pinpoint_user_activity.activity_type = str(data['activity_type'])
        pinpoint_user_activity.latitude = None if str(data['latitude']) == '' else float(data['latitude'])
        pinpoint_user_activity.longitude = None if str(data['longitude']) == '' else float(data['longitude'])
        pinpoint_user_activity.the_geom = "Point()"

        try:
            pinpoint_user_activity.save()
        except (AssertionError, AttributeError) as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)


class VisitorCreateAPIView(APIView):

    def post(self, request, format=None):

        data = request.data

        visitor = Visitor()
        visitor.user = None if request.user.id is None else request.user
        visitor.page_name = str(request.environ['PATH_INFO'])
        visitor.latitude = None if str(data['latitude']) == '' else float(data['latitude'])
        visitor.longitude = None if str(data['longitude']) == '' else float(data['longitude'])
        visitor.ip = str(request.environ['REMOTE_ADDR'])
        visitor.agent = str(request.environ['HTTP_USER_AGENT'])

        try:
            visitor.save()
        except (AssertionError, AttributeError) as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)


class LayerLoadCreateAPIView(APIView):

    def post(self, request, format=None):

        data = request.data

        layer_load = LayerLoad()
        layer_load.user = None if request.user.id is None else request.user
        layer_load.layer = None if str(data['layer']) == '' else Layer.objects.get(id=int(data['layer']))
        layer_load.latitude = None if str(data['latitude']) == '' else float(data['latitude'])
        layer_load.longitude = None if str(data['longitude']) == '' else float(data['longitude'])
        layer_load.ip = str(request.environ['REMOTE_ADDR'])
        layer_load.agent = str(request.environ['HTTP_USER_AGENT'])

        try:
            layer_load.save()
        except (AssertionError, AttributeError) as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)


class MapLoadCreateAPIView(APIView):

    def post(self, request, format=None):

        data = request.data

        map_load = MapLoad()
        map_load.user = None if request.user.id is None else request.user
        map_load.map = Map.objects.get(id=int(data['map']))
        map_load.latitude = None if str(data['latitude']) == '' else float(data['latitude'])
        map_load.longitude = None if str(data['longitude']) == '' else float(data['longitude'])
        map_load.ip = str(request.environ['REMOTE_ADDR'])
        map_load.agent = str(request.environ['HTTP_USER_AGENT'])

        try:
            map_load.save()
        except (AssertionError, AttributeError) as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)


class MapListAPIView(AnalyticsMixin, ListAPIView):
    """
    Will send summary of Map activity
    """
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get_queryset(self):
        content_model = ContentType.objects.get_for_model(Map)
        return LoadActivity.objects.filter(content_type=content_model).order_by('last_modified')

    def get(self, request, **kwargs):
        keys = ['map_id', 'last_modified_date', 'activity_type']

        map_load_data = self.format_data(query=self.get_queryset())
        pin_point_data = self.format_data(model_instance=PinpointUserActivity, filters=dict(map_id__isnull=False))

        results = self.get_analytics(map_load_data, ['object_id','last_modified_date', 'activity_type']) + self.get_analytics(pin_point_data, keys)

        return Response(data=self.filter_response(Map, 'map', results), status=status.HTTP_200_OK)


class LayerListAPIView(AnalyticsMixin, ListAPIView):
    """
    Will send summary of Layer activity
    """
    permission_classes = (IsAuthenticated, IsAdminUser,)
    
    def get_queryset(self):
        content_model = ContentType.objects.get_for_model(Layer)
        return LoadActivity.objects.filter(content_type=content_model).order_by('last_modified')

    def get(self, request, **kwargs):
        keys = ['layer_id', 'last_modified_date', 'activity_type']
        layer_load_data = self.format_data(query=self.get_queryset())
        pin_point_data = self.format_data(model_instance=PinpointUserActivity, filters=dict(layer_id__isnull=False))

        results = self.get_analytics(layer_load_data, ['object_id','last_modified_date', 'activity_type']) + self.get_analytics(pin_point_data, keys)
        
        return Response(data=self.filter_response(Layer, 'layer', results), status=status.HTTP_200_OK)
    

class DocumentListAPIView(AnalyticsMixin, ListAPIView):
    """
    Will send summary of Layer activity
    """
    permission_classes = (IsAuthenticated, IsAdminUser,)
    
    def get_queryset(self):
        content_model = ContentType.objects.get_for_model(Document)
        return LoadActivity.objects.filter(content_type=content_model).order_by('last_modified')        

    def get(self, request, **kwargs):
        keys = ['object_id', 'last_modified_date', 'activity_type']

        document_load_data = self.format_data(query=self.get_queryset(),extra_field=dict(activity_type='load'))
        
        results = self.get_analytics(document_load_data, keys)
        return Response(data=self.filter_response(Document, 'document', results), status=status.HTTP_200_OK)


class NonGISActivityCreateAPIView(CreateAPIView):
    """
    """
    def _save(self, content_object, ip, activity_type, agent,latitude=None, longitude=None, user=None):
        obj = LoadActivity(content_object=content_object, 
                            ip=ip, agent=agent, 
                            activity_type=activity_type,
                            latitude=float(latitude) if latitude else None, 
                            longitude= float(longitude) if longitude else None, 
                            user=user if user is not None and user.id is not None else None)
        obj.save()

    def post(self, request, **kwargs):
        data = request.data
        content_type = kwargs.get('content_type', data.get('content_type', None))

        if content_type is None:
            raise Exception('Unable to determine the the activity type')
        
        model_instance = ContentTypeEnum.CONTENT_TYPES.get(content_type, None)
        
        if not model_instance:
            raise Exception('Invalid activity action')
        
        content_object = model_instance.objects.get(pk=data.get('id'))
        
        self._save(content_object=content_object, 
                ip = str(request.environ['REMOTE_ADDR']),
                agent = str(request.environ['HTTP_USER_AGENT']),
                activity_type = data.get('activity_type', None),
                user = None if request.user.id is None else request.user,
                latitude = data.get('latitude', None),
                longitude = data.get('longitude', None)
                )

        return Response(status=status.HTTP_201_CREATED)

class GISActivityCreateAPIView(CreateAPIView):
    """
    """
    def _save(self, ip, agent, activity_type, map_id=None, layer_id=None,latitude=None, longitude=None, user=None):
        obj = PinpointUserActivity(ip=ip, 
                            agent=agent,  
                            activity_type = activity_type,
                            map_id = None if map_id is None else int(map_id),
                            layer_id = None if layer_id is None else int(layer_id),
                            latitude=float(latitude) if latitude is not None else None, 
                            longitude= float(longitude) if longitude is not None else None, 
                            user=user if user is not None and user.id is not None else None,
                            the_geom= "POINT({0} {1})".format(longitude,latitude))
        obj.save()

    def post(self, request, **kwargs):
        for data in request.data:      
            self._save(
                    ip = str(request.environ['REMOTE_ADDR']),
                    agent = str(request.environ['HTTP_USER_AGENT']),
                    activity_type= data.get('activity_type'),
                    map_id= data.get('map_id', None),
                    layer_id= data.get('layer_id', None),
                    latitude = data.get('latitude', None),
                    longitude = data.get('longitude', None),
                    user = None if request.user.id is None else request.user,
                    )

        return Response(status=status.HTTP_201_CREATED)

class SummaryAPIView(ListAPIView):
    """
    Send analytics summary
    """
    permission_classes = (IsAuthenticated, IsAdminUser,)
    def _GisActivity(self, filter):
        try:
            return PinpointUserActivity.objects.filter(**filter).values('activity_type').annotate(total=Count('activity_type'))
        except Exception:
            return []

    def _ActivityByContentModel(self, model):
        try:
            content_model = ContentType.objects.get_for_model(model)        
            return LoadActivity.objects.filter(content_type=content_model).values('activity_type').annotate(total=Count('activity_type'))
        except Exception:
            return []
    
    def _getAnalytics(self, model, filter):
        gis = self._GisActivity(filter)
        no_gis = self._ActivityByContentModel(model)

        response = dict()
        for k in list(gis)+list(no_gis):
            response.update({k["activity_type"]:k["total"]})
        return response
        
    def list(self, request):
        return Response(dict(map=self._getAnalytics(Map, dict(map_id__isnull=False)), 
                        layer=self._getAnalytics(Layer, dict(layer_id__isnull=False)),
                        document=self._getAnalytics(Document, dict(document_id__isnull=False))))
