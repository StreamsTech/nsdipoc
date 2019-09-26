import shutil

from django.contrib.gis.db import models
from django.db import transaction

from geonode.class_factory import ClassFactory
from geonode.layers.models import Layer
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from django.utils.translation import ugettext as _

from geonode.rest_authentications import CsrfExemptSessionAuthentication
from rest_framework.response import Response
from rest_framework import status
from geonode.groups.models import GroupProfile
from geonode.layers.api.utils import updateBoundingBox, getShapeFileFromAttribute, uploadLayer, changeDbFieldTypes, reloadFeatureTypes
from geonode.nsdi.utils import get_organization
from geonode.layers.views import _resolve_layer

_PERMISSION_MSG_VIEW = _("You are not permitted to update this layer")


class LayerFeatureUploadView(CreateAPIView):
    '''
    This API class receives a layer feature as json input
    and processes that feature to upload to postgis database
    directly to the specified layer.
    '''
    _EXTRA_FIELD = {'USER-DEFINED': models.GeometryField, "date": models.DateTimeField}
    permission_classes = (IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def post(self, request, pk, **kwargs):
        out = dict(success=True)
        status_code = status.HTTP_201_CREATED
        factory = ClassFactory(self._EXTRA_FIELD)
        try:
            layer = Layer.objects.get(id=pk)
            layer = _resolve_layer(
                request,
                layer.typename,
                'base.view_resourcebase',
                _PERMISSION_MSG_VIEW)
            model_instance = factory.get_model(name=str(layer.title_en), 
                                                table_name=str(layer.name),
                                                db=str(layer.store))
            with transaction.atomic(using=str(layer.store)):
                for feature in request.data:
                    obj = model_instance(**feature)
                    obj.save()

                #update bbox for the layer according to the
                #updated feature
                updateBoundingBox(layer)

        except Layer.DoesNotExist:
            out['success'] = False
            out['errors'] = "Layer Does not exist with this id"
            status_code = status.HTTP_404_NOT_FOUND
        except Exception as ex:
            out['success'] = False
            out['error'] = ex.message
            status_code = status.HTTP_400_BAD_REQUEST

        return Response(data=out, content_type='application/json', status=status_code)


class CreateFeaturedLayer(CreateAPIView):
    '''
    This API class receives a json string with a layer
    credentials and attributes for a feature and
    creates an empty layer without any vector data and
    only with attributes and sends layer id in response.
    '''
    permission_classes = (IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def post(self, request, **kwargs):
        out = {'success': True}
        status_code = status.HTTP_201_CREATED

        layer_title = request.data.get('layer_title')

        group = get_organization(request.user)

        keywords = []
        if layer_title is not None and len(layer_title) > 0:
            keywords = layer_title.split()

        base_file, tempdir = getShapeFileFromAttribute(**request.data)
        saved_layer = uploadLayer(base_file=base_file, user=request.user, group=group, keywords=keywords, user_data_epsg=4326, **request.data)

        #primarily all the columns of the saved_layer is character variyng
        #now we should change column types according to given types
        #this method below does this task
        changeDbFieldTypes(saved_layer, **request.data)

        ## after changing column types in postgis it is
        ## needed to reload this to geoserver
        ## this method does this task
        reloadFeatureTypes(saved_layer)

        saved_layer.current_version = 1
        saved_layer.latest_version = 1
        saved_layer.geometry_type = request.data.get('layer_type').lower()
        saved_layer.save()
        permissions = request.data.get('permissions')
        if permissions is not None and len(permissions.keys()) > 0:
            saved_layer.set_permissions(permissions)
        out['layer_id'] = saved_layer.id

        if not saved_layer:
            out['success'] = False
            out['error'] = "Can not create layer with provided credentials"
            status_code = status.HTTP_400_BAD_REQUEST

        if tempdir is not None:
            shutil.rmtree(tempdir)

        return Response(data=out, content_type='application/json', status=status_code)