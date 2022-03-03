from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from geonode.nsdi.utils import get_organization
from models import WorkshopTraining
# from forms import DataProductSpecificationUploadForm


class WorkshopTrainingListView(TemplateView):
    """
    This view is for Workshop/Training list view
    """

    template_name = 'workshop_training_list.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(WorkshopTrainingListView, self).dispatch(*args, **kwargs)
