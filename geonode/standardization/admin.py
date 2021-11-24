from django.contrib import admin

# Register your models here.

from .models import  DPSDocumentType, DataProductSpecification
admin.site.register(DPSDocumentType)
admin.site.register(DataProductSpecification)
