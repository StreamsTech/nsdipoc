from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from models import UserFeedback
from forms import NsdiUserFeedbackCreateUpdateForm, AnonymousUserFeedbackCreateUpdateForm
# Create your views here.


class UserFeedbackList(ListView):
    """
    This view lists all the user feedbacks
    """
    template_name = 'user_feedback_list.html'
    model = UserFeedback

    def get_queryset(self):
        return UserFeedback.objects.all().order_by('-date_created')[:15]


# @method_decorator(login_required)
class UserFeedbackCreate(SuccessMessageMixin, CreateView):
    """
    This view is for creating new news
    """


    template_name = 'user_feedback_create.html'
    model = UserFeedback
    success_message = "Your feedback sent successfully"

    def get_success_url(self):
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

