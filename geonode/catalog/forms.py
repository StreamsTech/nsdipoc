from django import forms
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions

from suit.widgets import HTML5Input


# from models import UserFeedback
from geonode.catalog.models import DataCatalog

class DataCatalogCreateUpdateForm(forms.ModelForm):

    class Meta:
        model = DataCatalog
        exclude = ['date_created', 'date_updated', 'ownership']




