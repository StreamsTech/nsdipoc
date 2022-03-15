import requests
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader
from django.http import HttpResponseForbidden
from django.http import Http404

from geonode.authentication_decorators import document_delete_permission_required
from geonode.nsdi.utils import get_organization
from models import WorkshopTraining, WorkshopDay, DAY_TYPE_SLUGS, WorkshopDocument
from forms import WorkshopCreateForm, WorkshopDocumentCreateForm


class WorkshopTrainingListView(TemplateView):
    """
    This view is for Workshop/Training list view
    """

    template_name = 'workshop_training_list.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(WorkshopTrainingListView, self).dispatch(*args, **kwargs)


class WorkshopTrainingDetailsView(TemplateView):
    """
    This view gives the details of a news
    """
    template_name = 'workshop_training_detail.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(WorkshopTrainingDetailsView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(WorkshopTrainingDetailsView, self).get_context_data(**kwargs)
        context['workshop_pk'] = kwargs['workshop_pk']
        return context


class WorkshopTrainingCreateView(CreateView):
    """
    This view is for creating new WorkshopTraining
    """
    template_name = 'workshop_training_create.html'
    model = WorkshopTraining
    form_class = WorkshopCreateForm

    def dispatch(self, request, *args, **kwargs):
        response = super(WorkshopTrainingCreateView, self).dispatch(request, *args, **kwargs)
        if not self.request.user.is_superuser:
            return HttpResponseRedirect(reverse('workshop-training-list'))
        else:
            return response

    def get_success_url(self):
        for day in range(self.object.days + 1):
            type = DAY_TYPE_SLUGS[day]
            WorkshopDay.objects.create(type=type[0], training_course=self.object)
        return reverse('workshop-training-list')


class WorkshopTrainingDocumentCreateView(CreateView):
    """
    This view is for creating new WorkshopTraining Document
    """
    template_name = 'workshop_training_document_create.html'
    model = WorkshopDocument

    def get_success_url(self):
        return reverse('workshop-training-details', kwargs={'workshop_pk': self.kwargs['workshop_pk']})

    def get_form_class(self):
        return WorkshopDocumentCreateForm

    def get_form_kwargs(self):
        kwargs = super(WorkshopTrainingDocumentCreateView, self).get_form_kwargs()
        kwargs['workshop_pk'] = self.kwargs['workshop_pk']
        kwargs['user_id'] = self.request.user.id
        return kwargs


class WorkshopTrainingDocumentDetailsView(DetailView):
    """
    This view gives the details of a Workshop training document
    """
    template_name = 'document_details.html'

    def get_object(self):
        return WorkshopDocument.objects.get(pk=self.kwargs['document_pk'])


class WorkshopTrainingDocumentEditView(UpdateView):
    template_name = 'workshop_training_document_update.html'
    model = WorkshopDocument
    form_class = WorkshopDocumentCreateForm

    def get_object(self):
        return WorkshopDocument.objects.get(pk=self.kwargs['document_pk'])

    def get_success_url(self):
        return reverse('workshop-training-details', kwargs={'workshop_pk': self.kwargs['workshop_pk']})

    def get_form_kwargs(self):
        kwargs = super(WorkshopTrainingDocumentEditView, self).get_form_kwargs()
        kwargs['workshop_pk'] = self.kwargs['workshop_pk']
        kwargs['user_id'] = self.request.user.id
        return kwargs


class WorkshopTrainingDocumentDeleteView(DeleteView):
    template_name = 'document_delete.html'
    model = WorkshopDocument

    def get_success_url(self):
        return reverse('workshop-training-details', kwargs={'workshop_pk': self.kwargs['workshop_pk']})

    @method_decorator(login_required)
    @method_decorator(document_delete_permission_required)
    def dispatch(self, request, *args, **kwargs):
        return super(WorkshopTrainingDocumentDeleteView, self).dispatch(request, *args, **kwargs)

    def get_object(self):
        id = self.kwargs['document_pk']
        return get_object_or_404(WorkshopDocument, id=id)

    def get_context_data(self, **kwargs):
        context = super(WorkshopTrainingDocumentDeleteView, self).get_context_data(**kwargs)
        context['workshop_pk'] = self.kwargs['workshop_pk']
        return context
