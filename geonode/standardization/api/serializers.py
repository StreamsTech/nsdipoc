import json

from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from geonode.data_upload.models import StatusUpdateModel, MasterData, BillingData, DeepTubewellData, DmaNrw, \
    ScadaStatus, BulkMeterReading


class StatusUpdateSerializer(ModelSerializer):
    """
    Model serializer for Status Update Model
    """

    errors = serializers.SerializerMethodField()
    uploader = serializers.SerializerMethodField()
    upload_time = serializers.SerializerMethodField()

    class Meta:
        model = StatusUpdateModel
        fields = ('id', 'uploader', 'file_name', 'upload_status', 'errors', 'upload_time')

    def get_errors(self, status):
        return eval(status.errors)

    def get_uploader(self, status):
        return status.uploader.username

    def get_upload_time(self, status):
        return str(status.date_updated.date()) + " " + str(status.date_updated.hour) +":"+ str(status.date_updated.minute) +":"+ str(status.date_updated.second)


class MasterDataSerializer(ModelSerializer):
    """
    Model serializer for Master Data Model
    """
    class Meta:
        model = MasterData
        fields = '__all__'


class BillingDataSerializer(ModelSerializer):
    """
    Model serializer for Billing Data Model
    """

    class Meta:
        model = BillingData
        fields = '__all__'


class DeepTubewellDataSerializer(ModelSerializer):
    """
    Model serializer for Deep Tubewell Model
    """

    class Meta:
        model = DeepTubewellData
        fields = '__all__'


class DmaNrwSerializer(ModelSerializer):
    """
    Model serializer for DmaNrw Model
    """

    class Meta:
        model = DmaNrw
        fields = '__all__'


class SCADASerializer(ModelSerializer):
    """
    Model serializer for ScadaReading Model
    """

    class Meta:
        model = ScadaStatus
        fields = '__all__'


class BulkMeterReadingSerializer(ModelSerializer):
    """
    Model serializer for BulkMeterReading Model
    """

    class Meta:
        model = BulkMeterReading
        fields = '__all__'


from geonode.standardization.models import DataProductSpecification
class DPSSerializer(ModelSerializer):
    """
    Model serializer for BulkMeterReading Model
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
