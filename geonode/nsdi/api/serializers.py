from rest_framework import serializers
from geonode.nsdi.models import SectorModel, DepartmentModel
from geonode.groups.models import GroupProfile


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupProfile
        fields = ('title','slug',)



class DepartmentSerializer(serializers.ModelSerializer):
    organizations = OrganizationSerializer(many=True, read_only=True)
    class Meta:
        model = DepartmentModel
        fields = ('title', 'organizations',)


class SectorSerializer(serializers.ModelSerializer):
    # title = serializers.CharField()
    departments = DepartmentSerializer(many=True, read_only=True)

    class Meta:
        model = SectorModel
        fields = ('title','departments',)