from rest_framework import serializers

from geonode.layers.models import Layer


class LayersListSearchSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Layer
        fields = [
        # fields in the db
        'id',
        'uuid',
        'title',
        'date',
        'abstract',
        'csw_wkt_geometry',
        'csw_type',
        'owner',
        'share_count',
        'popular_count',
        'srid',
        'category',
        'supplemental_information',
        'thumbnail_url',
        'detail_url',
        'rating',
        'bbox_x0',
        'bbox_x1',
        'bbox_y0',
        'bbox_y1',

    ]