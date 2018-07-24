
from rest_framework.serializers import ModelSerializer
from geonode.feedback.models import UserFeedback


class NsdiUserFeedbackCreateSerializer(ModelSerializer):
    """
    This serializer serializes object of UserFeedback model
    when requested user is a NSDI user.
    NSDI user is allowed to input only title, message and attachment
    other info will be gathered from Profile model
    """
    class Meta:
        model = UserFeedback
        fields = ('title', 'message', 'attachment')

    def create(self, validated_data):
        """
        serializers create method is overrided here.
        because logged_in users will not provide name, email and contact no.
        these info will be gathered from user model
        """
        feedback = UserFeedback.objects.create(**validated_data)
        user = self.context['request'].user
        if user.is_authenticated:
            feedback.commenter_email = user.email
            feedback.commenter_name = user.username
            feedback.contact_no = user.contact_no
        feedback.save()
        return feedback



class AnonymousUserFeedbackCreateSerializer(ModelSerializer):
    """
    This serializer serializes object of UserFeedback model when
    an anonymous user tries feedback.
    """

    class Meta:
        model = UserFeedback
        fields = ('commenter_name', 'commenter_email', 'contact_no', 'title', 'message', 'attachment')


class UserFeedbackListSerializer(ModelSerializer):
    """
    This serializer is using for listing all the user feedbacks.
    Only Committee members are allowed to view the feedback list.
    """

    class Meta:
        model = UserFeedback
        exclude = ('slug',)