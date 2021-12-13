from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from geonode.standardization.models import DataProductSpecification


class DPSSerializer(ModelSerializer):
    """
    Model serializer for DPS Model
    """
    organization = serializers.SerializerMethodField()
    document_type = serializers.SerializerMethodField()

    class Meta:
        model = DataProductSpecification
        fields = ('id', 'doc_file', 'organization', 'document_type', 'title', 'creation_date')

    def get_organization(self, dps):
        return dps.organization.title

    def get_document_type(self, dps):
        return dps.document_type.name
