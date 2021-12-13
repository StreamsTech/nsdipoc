from django import forms

from models import DataProductSpecification


class DateInput(forms.DateInput):
    input_type = 'date'


class DataProductSpecificationUploadForm(forms.ModelForm):
    class Meta:
        model = DataProductSpecification
        fields = ['document_type', 'title', 'creation_date', 'version', 'remarks', 'doc_file']
        widgets = {
            'creation_date': DateInput(),
        }
