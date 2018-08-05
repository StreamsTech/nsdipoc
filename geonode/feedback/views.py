from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.http import Http404, HttpResponseForbidden, HttpResponseRedirect, HttpResponseNotAllowed, HttpResponse
from django.template import RequestContext, loader


from models import UserFeedback
from forms import NsdiUserFeedbackCreateUpdateForm, AnonymousUserFeedbackCreateUpdateForm
from geonode.base.libraries.decorators import superuser_check
# Create your views here.


class UserFeedbackList(ListView):
    """
    This view lists all the user feedbacks
    """
    template_name = 'user_feedback_list.html'
    model = UserFeedback

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if superuser_check(self.request.user):
            return super(UserFeedbackList, self).dispatch(*args, **kwargs)
        else:
            return HttpResponse(
                loader.render_to_string(
                    '404.html', RequestContext(
                        self.request, {
                        })), status=404)

    def get_queryset(self):
        return UserFeedback.objects.all().order_by('-date_created')[:15]


class UserFeedbackCreate(SuccessMessageMixin, CreateView):
    """
    This view is for creating new user feedback
    """


    template_name = 'user_feedback_create.html'
    model = UserFeedback
    success_message = "Your feedback has been successfully"

    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return reverse('user_feedback_create')


    def get_form_class(self):
        if self.request.user.is_authenticated():
            return NsdiUserFeedbackCreateUpdateForm
        else:
            return AnonymousUserFeedbackCreateUpdateForm

    def form_valid(self, form):
        if self.request.user.is_authenticated():
            self.object = form.save(commit=False)
            if not self.object.commenter_name:
                self.object.commenter_name = self.request.user.username
            if not self.object.commenter_email:
                self.object.commenter_email = self.request.user.email
            if not self.object.contact_no:
                self.object.contact_no = self.request.user.contact_no
            self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class UserFeedbackDetails(DetailView):
    """
    This view gives the details of a user feedback
    """
    template_name = 'user_feedback_details.html'

    def get_object(self):
        return UserFeedback.objects.get(pk=self.kwargs['feedback_pk'])


class UserFeedbackDelete(DeleteView):
    """
    This view is for deleting an existing user feedback
    """
    template_name = 'user_feedback_delete.html'
    model = UserFeedback
    success_message = "Deleted selected user feedback successfully"

    def dispatch(self, request, *args, **kwargs):
        response = super(UserFeedbackDelete, self).dispatch(request, *args, **kwargs)
        if not self.request.user.is_superuser:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return response

    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return reverse('user_feedback_list')

    def get_object(self):
        return UserFeedback.objects.get(pk=self.kwargs['feedback_pk'])
