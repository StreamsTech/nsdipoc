from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from geonode.workshop_training.models import WorkshopTraining, WorkshopDocument, WorkshopDay


class WorkshopTrainingSerializer(ModelSerializer):
    """
    Model serializer for WorkshopTraining Model
    """
    workshop_date_format = serializers.SerializerMethodField()
    class Meta:
        model = WorkshopTraining
        fields = ('id', 'title','date_from', 'date_to', 'overview', 'days', 'workshop_date_format')

    def get_workshop_date_format(self, workshop):
        if workshop.days == 1:
            return "Date: "+ workshop.date_from.strftime("%m %b, %Y")
        if workshop.days == 2:
            return "Date: " + workshop.date_from.strftime("%m %b") + " and " + workshop.date_to.strftime("%m %b, %Y")
        return "Date: From " + workshop.date_from.strftime("%m %b") + " to " + workshop.date_to.strftime("%m %b, %Y")


class WorkshopDocumentSerializer(ModelSerializer):
    organization = serializers.SerializerMethodField()
    date_created = serializers.SerializerMethodField()
    editable = serializers.SerializerMethodField()

    class Meta:
        model = WorkshopDocument
        fields = '__all__'

    def get_organization(self, document):
        return document.organization.title

    def get_date_created(self, document):
        return document.date_created.strftime("%m %b, %Y")

    def get_editable(self, document):
        request = self.context.get("request")
        user = None
        if request and hasattr(request, "user"):
            user = request.user
        if user and user == document.user:
            return True
        return False


class WorkshopDaySerializer(ModelSerializer):
    documents = WorkshopDocumentSerializer(many=True, read_only=True)
    class Meta:
        model = WorkshopDay
        fields = '__all__'
        depth = 3
        ordering = ['pk']


class WorkshopDocumentListSerializer(ModelSerializer):
    """
    Model serializer for WorkshopTraining Document Model
    """
    workshop_days = WorkshopDaySerializer(many=True, read_only=True)

    class Meta:
        model = WorkshopTraining
        fields = ('id', 'title', 'workshop_days')
        depth = 3

    def to_representation(self, instance):
        response = super(WorkshopDocumentListSerializer, self).to_representation(instance)
        response["workshop_days"] = sorted(response["workshop_days"], key=lambda x: x["type"])
        return response
