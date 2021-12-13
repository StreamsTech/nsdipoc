from django.db import models

# Create your models here.
from geonode.groups.models import GroupProfile
from geonode.people.models import Profile


class DPSDocumentType(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class DataProductSpecification(models.Model):
    """
    This model is for data product specification management
    """
    user = models.ForeignKey(Profile, related_name="dps")
    organization = models.ForeignKey(GroupProfile, related_name="dps")
    document_type = models.ForeignKey(DPSDocumentType, related_name="dps", verbose_name="Type of document")
    title = models.CharField(max_length=200)
    creation_date = models.DateTimeField()
    version = models.CharField(max_length=20, blank=True, null=True)
    remarks = models.TextField(max_length=300, blank=True, null=True)
    doc_file = models.FileField(upload_to='dps_files')
    is_active = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
