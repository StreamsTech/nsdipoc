
from rest_framework.generics import ListCreateAPIView

from geonode.rest_authentications import CsrfExemptSessionAuthentication
from serializers import NsdiUserFeedbackCreateSerializer, AnonymousUserFeedbackCreateSerializer, UserFeedbackListSerializer
from geonode.feedback.models import UserFeedback

# Create your views here.


class UserFeedbackCreateAPIView(ListCreateAPIView):
    """
    This API is for creating and listing user feedbacks.
    Anyone can send a feedback.
    Only committee members can view the list of feedbacks.
    """
    
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserFeedbackListSerializer
        if self.request.user.is_authenticated() and self.request.method == 'POST':
            return NsdiUserFeedbackCreateSerializer
        return AnonymousUserFeedbackCreateSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated() and self.request.user.is_working_group_admin:
            return UserFeedback.objects.filter(is_active=True)
        return UserFeedback.objects.none()
