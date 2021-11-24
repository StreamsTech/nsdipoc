from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from forms import DataProductSpecificationUploadForm
from geonode.nsdi.utils import get_organization


from models import DataProductSpecification


class DPSListView(TemplateView):
    template_name = 'dps_list.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(DPSListView, self).dispatch(*args, **kwargs)


class DPSCreateView(CreateView):
    """
    This view is for creating new news
    """
    template_name = 'dps_upload.html'
    model = DataProductSpecification

    def form_valid(self, form):
        self.object = form.save(commit=False)
        # self.object.section = SectionManagementTable.objects.get(pk=self.kwargs['section_pk'])
        user = self.request.user
        organization = get_organization(user)
        self.object.user = user
        self.object.organization = organization
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('nsdi-dps-list')

    def get_form_class(self):
        return DataProductSpecificationUploadForm
