from django import forms
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions

from suit.widgets import HTML5Input


from models import UserFeedback
from geonode.cms.models import FooterSectionDescriptions
from geonode.local_settings import slider_image_dimension


class NsdiUserFeedbackCreateUpdateForm(forms.ModelForm):

    class Meta:
        model = UserFeedback
        fields = ['title', 'message', 'attachment']



class AnonymousUserFeedbackCreateUpdateForm(forms.ModelForm):

    class Meta:
        model = UserFeedback
        fields = ['commenter_name', 'commenter_email', 'contact_no', 'title', 'message', 'attachment']
