from geonode.geoserver.mixins import GeoServerMixin
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response


from geonode.layers.views import _resolve_layer, _PERMISSION_MSG_VIEW


class GeoserverWMSGetFeatureInfoListAPIView(ListAPIView, GeoServerMixin):
    """
    This api will serve wms call of geoserver
    """
    
    def get(self, request, **kwargs):
        data = dict(request.query_params)
        layers = data.get('layers', [None])[0]

        if not layers:
            layers = data.get('LAYERS')[0]

        access_token = None
        if 'access_token' in request.session:
            access_token = request.session['access_token']

        query = self.get_configuration(data)
        result = dict()
        for layer_name in layers.split(','):
            layer_obj = _resolve_layer(request,
                                       layer_name,
                                       'base.view_resourcebase',
                                       _PERMISSION_MSG_VIEW)
            if request.user in layer_obj.group.get_members():
                attributes = self.getOwnerAttributesPermission(layer_name=layer_name)
            else:
                attributes = self.getAttributesPermission(layer_name=layer_name)
            if 'the_geom' in attributes:
                attributes.remove('the_geom')
            query.update(dict(SERVICE='WMS', 
                            REQUEST='GetFeatureInfo',
                            QUERY_LAYERS= layer_name,
                            LAYERS=layer_name,
                            access_token=access_token, 
                            propertyName=','.join(attributes)))
            result[layer_name] = self.get_response_from_geoserver('wms', query)
        
        response = dict()
        for k,v in result.items():
            if not response:
                response = v
            else:
                if 'features' in v:
                    response['features'] += v['features']

        return Response(response, status=status.HTTP_200_OK)
