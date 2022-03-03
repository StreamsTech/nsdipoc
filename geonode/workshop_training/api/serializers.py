from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from geonode.workshop_training.models import WorkshopTraining


class WorkshopTrainingSerializer(ModelSerializer):
    """
    Model serializer for WorkshopTraining Model
    """

    class Meta:
        model = WorkshopTraining
        fields = ('id', 'date_from', 'date_to', 'overview')
