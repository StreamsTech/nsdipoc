import json
import requests
import urllib
from django.conf import settings
from geonode.layers.models import Layer


class GeoServerMixin(object):
    """
    Mixing for GeoServer
    """
    def get_configuration(self, data):
        query = {}
        for k,v in data.items():
            query.update({k: v[0] if type(v) == list else v})
        return query

    def get_response_from_geoserver(self, api_type, query, layername):
        url = settings.GEOSERVER_LOCATION + api_type
        response = requests.get('{}?{}'.format(url, urllib.urlencode(query)))
        if query['request'] == 'describeFeatureType':
            return get_response(layername, json.loads(response.content))
        else:
            return json.loads(response.content)

    def getAttributesPermission(self, layer_name):
        attributes = [ l.attribute for l in Layer.objects.get(typename=layer_name).attribute_set.all() if l.is_permitted ]

        return attributes



def get_response(layer_name, response):
    permitted_attributes = [ l.attribute for l in Layer.objects.get(typename=layer_name).attribute_set.all() if l.is_permitted ]
    response_list = response
    import pdb; pdb.set_trace()
    for i in xrange(len(response['featureTypes'][0]['properties'])):
        if  response['featureTypes'][0]['properties'][i]['name'] not in permitted_attributes:
            val =response['featureTypes'][0]['properties'][i]
            response_list['featureTypes'][0]['properties'].remove(val)

    return response_list

