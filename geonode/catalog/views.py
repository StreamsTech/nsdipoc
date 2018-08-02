from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, View, FormView
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import Http404, HttpResponseForbidden, HttpResponseRedirect, HttpResponseNotAllowed, HttpResponse
from django.template import RequestContext, loader
from django.utils.translation import ugettext as _
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings



from models import DataCatalog
from geonode.groups.models import GroupProfile
from forms import DataCatalogCreateUpdateForm
from geonode.authentication_decorators import manager_required

# Create your views here.


class DataCatalogList(ListView):
    """
    This view lists all the user feedbacks
    """
    template_name = 'data_catalog_list.html'
    model = DataCatalog

    def get_queryset(self):
        organization  = GroupProfile.objects.get(slug=self.kwargs['org'])
        return DataCatalog.objects.filter(ownership=organization).order_by('-date_created')[:100]

    def get_context_data(self, **kwargs):
        context = super(DataCatalogList, self).get_context_data(**kwargs)
        organization = GroupProfile.objects.get(slug=self.kwargs['org'])
        if self.request.user.is_authenticated() and self.request.user in organization.get_managers():
            context['manager'] = True
        context['member'] = organization.user_is_member(self.request.user)
        context['org_slug'] = organization.slug

        return context






class DataCatalogCreate(SuccessMessageMixin,  CreateView):
    """
    This view is for creating new data catalog
    """

    template_name = 'data_catalog_create.html'
    model = DataCatalog
    success_message = "successful !"

    def get_success_url(self, slug):
        messages.success(self.request, self.success_message)
        return reverse('data_catalog_list', kwargs={'org': slug})

    @method_decorator(login_required)
    @method_decorator(manager_required)
    def dispatch(self, *args, **kwargs):
        return super(DataCatalogCreate, self).dispatch(*args, **kwargs)


    def get_form_class(self):
        return DataCatalogCreateUpdateForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        user_organization = GroupProfile.objects.filter(groupmember__user=self.request.user).exclude(slug='working-group')[0]
        self.object.ownership = user_organization
        self.object.save()
        return HttpResponseRedirect(self.get_success_url(user_organization.slug))


class DataCatalogUpdate(SuccessMessageMixin, UpdateView):
    template_name = 'data_catalog_create.html'
    model = DataCatalog
    form_class = DataCatalogCreateUpdateForm
    success_message = "successfully updated catalog !"

    @method_decorator(login_required)
    @method_decorator(manager_required)
    def dispatch(self, *args, **kwargs):
        return super(DataCatalogUpdate, self).dispatch(*args, **kwargs)

    def get_object(self):
        return DataCatalog.objects.get(pk=self.kwargs['cat_pk'])

    def get_success_url(self):
        user_organization = GroupProfile.objects.filter(groupmember__user=self.request.user).exclude(slug='working-group')[0]
        return reverse('data_catalog_list', kwargs={'org': user_organization.slug})

    def get_context_data(self, **kwargs):
        context = super(DataCatalogUpdate, self).get_context_data(**kwargs)
        user_organization = GroupProfile.objects.filter(groupmember__user=self.request.user).exclude(slug='working-group')[0]
        context['update'] = True
        context['slug'] = user_organization.slug
        return context




class DataCatalogDelete(DeleteView):
    template_name = 'data_catalog_delete.html'
    model = DataCatalog
    success_message = 'Catalog deleted successfully'

    def get_success_url(self):
        messages.success(self.request, self.success_message)
        user_organization = GroupProfile.objects.filter(groupmember__user=self.request.user).exclude(slug='working-group')[0]
        return reverse('data_catalog_list', kwargs={'org': user_organization.slug})

    @method_decorator(login_required)
    @method_decorator(manager_required)
    def dispatch(self, *args, **kwargs):
        return super(DataCatalogDelete, self).dispatch(*args, **kwargs)

    def get_object(self):
        return DataCatalog.objects.get(pk=self.kwargs['cat_pk'])

    def get_context_data(self, **kwargs):
        context = super(DataCatalogDelete, self).get_context_data(**kwargs)
        user_organization = GroupProfile.objects.filter(groupmember__user=self.request.user).exclude(slug='working-group')[0]
        context['slug'] = user_organization.slug
        if self.request.user.is_manager_of_any_group:
            context['manager'] = True
        return context


class CatDownloadRequest(SuccessMessageMixin, View):
    success_message = "Your request has been sent successfully!"

    def post(self, request, **kwargs):
        slug = self.kwargs['org']
        try:
            org = GroupProfile.objects.get(slug=slug)
        except GroupProfile.DoesNotExist:
                self.success_message = 'No organization found with this request'
                return HttpResponseRedirect(self.get_success_url())
        else:
            to_email = org.get_managers()[0].email
        layer_title = request.POST.get('title')
        if request.user.is_authenticated():
            email = request.user.email
            name = request.user.name
        else:
            email = request.POST.get('email')
            name = request.POST.get('name')

        message = request.POST.get('message')

        html_message = "<h3>"  + message
        html_message += "<br><br><br><br>Best regards,<br>Name: " + name + "<br>"
        html_message += "Email: " + email + "<br> <h3>"

        mail_subject = 'requesting for downloading layer,  ' + layer_title

        if layer_title and email and name and message:
            send_mail(subject=mail_subject, message=html_message, from_email=settings.EMAIL_FROM, recipient_list=[to_email],
                      fail_silently=False, html_message=html_message)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return reverse('data_catalog_list', kwargs={'org': 'orgA'})
