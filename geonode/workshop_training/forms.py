from django import forms
from django.forms import widgets
from models import WorkshopTraining, WorkshopDocument


class WorkshopCreateForm(forms.ModelForm):

    class Meta:
        model = WorkshopTraining
        fields = ['title', 'days', 'date_from', 'date_to', 'overview']
        widgets = {
            'date_from': widgets.DateInput(attrs={'type': 'date'}),
            'date_to': widgets.DateInput(attrs={'type': 'date'})
        }

class WorkshopDocumentCreateForm(forms.ModelForm):

    class Meta:
        model = WorkshopDocument
        fields = ['user', 'organization','title', 'doc_file', 'description']
        widgets = {
            'user': widgets.Select(attrs={'readonly': True, 'disabled':True})
        }

