from rest_framework import serializers

from geonode.layers.models import Layer
from geonode.base.models import ResourceBase


class ResourceBaseListSearchSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    organization_slug = serializers.ReadOnlyField(source='group.slug')
    organization_logo = serializers.ImageField(source='group.logo')
    category = serializers.ReadOnlyField(source='category.gn_description')
    can_make_featured = serializers.SerializerMethodField()

    def get_can_make_featured(self, obj):
        if self.context['request'].user in obj.group.get_managers():
            return True
        else:
            return False


    class Meta:
        model = ResourceBase
        fields = [
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
        'resource_type',
        'can_make_featured',
        'featured',
        'organization_slug',
        'organization_logo'

    ]