from django import forms
from django.forms import widgets
from models import WorkshopTraining, WorkshopDocument, WorkshopDay
from geonode.people.models import Profile
from geonode.nsdi.utils import get_organization
from geonode.groups.models import GroupProfile


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
        fields = ['user', 'organization', 'title', 'workshop_day', 'doc_file', 'description']
        widgets = {
            'user': widgets.Select(attrs={'readonly': True}),
            'organization': widgets.Select(attrs={'readonly': True})
        }

    def __init__(self, *args, **kwargs):
        self.workshop_pk = kwargs.pop('workshop_pk', None)
        self.user_id = kwargs.pop('user_id', None)
        self.user = Profile.objects.get(id=self.user_id)
        self.user_organization = get_organization(self.user)
        super(WorkshopDocumentCreateForm, self).__init__(*args, **kwargs)
        self.fields['user'].queryset = Profile.objects.filter(id=self.user_id)
        self.fields['user'].initial = self.user
        self.fields['organization'].initial = self.user_organization
        self.fields['organization'].queryset = GroupProfile.objects.filter(id=self.user_organization.id)
        self.fields['workshop_day'].queryset = WorkshopDay.objects.filter(training_course__id=self.workshop_pk)
