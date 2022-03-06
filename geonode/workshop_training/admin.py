from django.contrib import admin

from .models import  WorkshopTraining, WorkshopDocument, WorkshopDay


admin.site.register(WorkshopTraining)
admin.site.register(WorkshopDocument)
admin.site.register(WorkshopDay)
