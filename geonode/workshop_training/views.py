from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

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

    # def form_valid(self, form):
    #     self.object = form.save(commit=False)
    #     self.object.publish_date = form.data['publish_date']
    #     self.object.save()
    #     return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        for day in range(self.object.days + 1):
            type = DAY_TYPE_SLUGS[day]
            WorkshopDay.objects.create(type=type[0], training_course=self.object)
        return reverse('workshop-training-list')


class WorkshopTrainingDocumentCreateView(CreateView):
    """
    This view is for creating new WorkshopTraining
    """
    template_name = 'workshop_training_document_create.html'
    model = WorkshopDocument

    def get_success_url(self):
        return reverse('workshop-training-details', kwargs={'workshop_pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super(WorkshopTrainingDocumentCreateView, self).get_context_data(**kwargs)
        context['user_name'] = self.request.user.username
        context['organization'] = get_organization(self.request.user).title
        return context

    def get_form(self, form_class=None):
        initial = {
            'user': self.request.user
        }
        form_class = WorkshopDocumentCreateForm(data=initial)
        return form_class

