
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers
from guardian.shortcuts import get_objects_for_user
from avatar.templatetags.avatar_tags import avatar_url

from geonode.people.models import Profile
from geonode.layers.models import Layer
from geonode.maps.models import Map
from geonode.documents.models import Document


class UserSerializer(serializers.ModelSerializer):
    layers_count = serializers.SerializerMethodField('count_user_layers')
    maps_count = serializers.SerializerMethodField('count_user_maps')
    documents_count = serializers.SerializerMethodField('count_user_documents')
    profile_detail_url = serializers.SerializerMethodField('set_profile_detail_url')
    activity_stream_url = serializers.SerializerMethodField('set_activity_stream_url')
    avatar_100 = serializers.SerializerMethodField('set_avatar_100')
    current_user = serializers.SerializerMethodField('set_current_user')


    class Meta:
        model = Profile
        exclude = ("password", "last_login", "is_staff")


    def count_user_layers(self, obj):
        obj_with_perms = get_objects_for_user(obj,
                                              'base.view_resourcebase').instance_of(Layer)
        return obj.resourcebase_set.filter(id__in=obj_with_perms.values('id')).distinct().count()

    def count_user_maps(self, obj):
        obj_with_perms = get_objects_for_user(obj,
                                              'base.view_resourcebase').instance_of(Map)
        return obj.resourcebase_set.filter(id__in=obj_with_perms.values('id')).distinct().count()

    def count_user_documents(self, obj):
        obj_with_perms = get_objects_for_user(obj,
                                              'base.view_resourcebase').instance_of(Document)
        return obj.resourcebase_set.filter(id__in=obj_with_perms.values('id')).distinct().count()

    def set_profile_detail_url(self, obj):
        return obj.get_absolute_url()

    def set_activity_stream_url(self, obj):
        return reverse(
            'actstream_actor',
            kwargs={
                'content_type_id': ContentType.objects.get_for_model(
                    obj).pk,
                'object_id': obj.pk})

    def set_avatar_100(self, obj):
        return avatar_url(obj, 240)


    def set_current_user(self, obj):
        return obj.username == obj.username