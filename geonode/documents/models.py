# -*- coding: utf-8 -*-
#########################################################################
#
# Copyright (C) 2016 OSGeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#########################################################################

import logging
import os
import uuid
from urlparse import urlparse

from django.db import models
from django.db.models import signals
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.contrib.contenttypes import generic
from django.contrib.staticfiles import finders
from django.utils.translation import ugettext_lazy as _

from geonode.layers.models import Layer
from geonode.base.models import ResourceBase, resourcebase_post_save, Link
from geonode.documents.enumerations import DOCUMENT_TYPE_MAP, DOCUMENT_MIMETYPE_MAP
from geonode.maps.signals import map_changed_signal
from geonode.maps.models import Map
from geonode.security.models import remove_object_permissions

IMGTYPES = ['jpg', 'jpeg', 'tif', 'tiff', 'png', 'gif']

logger = logging.getLogger(__name__)


class Document(ResourceBase):

    """
    A document is any kind of information that can be attached to a map such as pdf, images, videos, xls...
    """

    # Relation to the resource model

    layers = models.ManyToManyField(Layer, blank=True, null=True, through='DocumentLayers', through_fields=('document', 'layer'))
    doc_file = models.FileField(upload_to='documents',
                                null=True,
                                blank=True,
                                max_length=255,
                                verbose_name=_('File'))

    extension = models.CharField(max_length=128, blank=True, null=True)

    doc_type = models.CharField(max_length=128, blank=True, null=True)

    doc_url = models.URLField(
        blank=True,
        null=True,
        max_length=255,
        help_text=_('The URL of the document if it is external.'),
        verbose_name=_('URL'))

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('document_detail', args=(self.id,))

    @property
    def name_long(self):
        if not self.title:
            return str(self.id)
        else:
            return '%s (%s)' % (self.title, self.id)

    def _render_thumbnail(self):
        from cStringIO import StringIO

        size = 200, 150

        try:
            from PIL import Image, ImageOps
        except ImportError, e:
            logger.error(
                '%s: Pillow not installed, cannot generate thumbnails.' %
                e)
            return None

        try:
            # if wand is installed, than use it for pdf thumbnailing
            from wand import image
        except:
            wand_available = False
        else:
            wand_available = True

        if wand_available and self.extension and self.extension.lower(
        ) == 'pdf' and self.doc_file:
            logger.debug(
                u'Generating a thumbnail for document: {0}'.format(
                    self.title))
            try:
                with image.Image(filename=self.doc_file.path) as img:
                    img.sample(*size)
                    return img.make_blob('png')
            except:
                logger.debug('Error generating the thumbnail with Wand, cascading to a default image...')
        # if we are still here, we use a default image thumb
        if self.extension and self.extension.lower() in IMGTYPES and self.doc_file:
            img = Image.open(self.doc_file.path)
            img = ImageOps.fit(img, size, Image.ANTIALIAS)
        else:
            filename = finders.find('documents/{0}-placeholder.png'.format(self.extension), False) or \
                finders.find('documents/generic-placeholder.png', False)

            if not filename:
                return None

            img = Image.open(filename)

        imgfile = StringIO()
        img.save(imgfile, format='PNG')
        return imgfile.getvalue()

    @property
    def class_name(self):
        return self.__class__.__name__

    class Meta(ResourceBase.Meta):
        pass


class DocumentLayers(models.Model):
    document = models.ForeignKey(Document)
    content_type = models.ForeignKey(ContentType, blank=True, null=True)
    layer = models.ForeignKey(Layer, blank=True, null=True)
    resource = generic.GenericForeignKey('content_type', 'layer')

    class Meta:
        db_table = 'document_layers'


def get_related_documents(resource):
    if isinstance(resource, Layer) or isinstance(resource, Map):
        ct = ContentType.objects.get_for_model(resource)
        # return Document.objects.filter(content_type=ct, object_id=resource.pk)
        return DocumentLayers.objects.filter(content_type_id=ct.id, layer_id=resource.id)
    else:
        return None


def pre_save_document(instance, sender, **kwargs):
    base_name, extension, doc_type = None, None, None

    if instance.doc_file:
        base_name, extension = os.path.splitext(instance.doc_file.name)
        instance.extension = extension[1:]
        doc_type_map = DOCUMENT_TYPE_MAP
        doc_type_map.update(getattr(settings, 'DOCUMENT_TYPE_MAP', {}))
        if doc_type_map is None:
            doc_type = 'other'
        else:
            doc_type = doc_type_map.get(instance.extension, 'other')
        instance.doc_type = doc_type

    elif instance.doc_url:
        if '.' in urlparse(instance.doc_url).path:
            instance.extension = urlparse(instance.doc_url).path.rsplit('.')[-1]

    if not instance.uuid:
        instance.uuid = str(uuid.uuid1())
    instance.csw_type = 'document'

    if instance.abstract == '' or instance.abstract is None:
        instance.abstract = 'Document abstract is very important! You are requested to update it now.'

    if instance.title == '' or instance.title is None:
        instance.title = instance.doc_file.name

    if getattr(instance, 'resource', None):
        instance.csw_wkt_geometry = instance.resource.geographic_bounding_box.split(
            ';')[-1]
        instance.bbox_x0 = instance.resource.bbox_x0
        instance.bbox_x1 = instance.resource.bbox_x1
        instance.bbox_y0 = instance.resource.bbox_y0
        instance.bbox_y1 = instance.resource.bbox_y1
    else:
        instance.bbox_x0 = -180
        instance.bbox_x1 = 180
        instance.bbox_y0 = -90
        instance.bbox_y1 = 90


def post_save_document(instance, *args, **kwargs):

    name = None
    ext = instance.extension
    mime_type_map = DOCUMENT_MIMETYPE_MAP
    mime_type_map.update(getattr(settings, 'DOCUMENT_MIMETYPE_MAP', {}))
    mime = mime_type_map.get(ext, 'text/plain')
    url = None

    if instance.doc_file:
        name = "Hosted Document"
        url = '%s%s' % (
            settings.SITEURL[:-1],
            reverse('document_download', args=(instance.id,)))
    elif instance.doc_url:
        name = "External Document"
        url = instance.doc_url

    if name and url:
        Link.objects.get_or_create(
            resource=instance.resourcebase_ptr,
            url=url,
            defaults=dict(
                extension=ext,
                name=name,
                mime=mime,
                url=url,
                link_type='data',))


def create_thumbnail(sender, instance, created, **kwargs):
    from geonode.tasks.update import create_document_thumbnail

    create_document_thumbnail(object_id=instance.id)


def update_documents_extent(sender, **kwargs):
    model = 'map' if isinstance(sender, Map) else 'layer'
    ctype = ContentType.objects.get(model=model)
    for document in Document.objects.filter(content_type=ctype, object_id=sender.id):
        document.save()


def pre_delete_document(instance, sender, **kwargs):
    remove_object_permissions(instance.get_self_resource())




#@jahangir
class DocumentSubmissionActivity(models.Model):
    """
    This model includes document submission activity
    """

    document = models.ForeignKey('documents.Document', related_name='document_submission')
    group = models.ForeignKey('groups.GroupProfile')
    iteration = models.IntegerField(default=0)
    is_audited = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


    class Meta:
        unique_together = (('document', 'group', 'iteration'),)

    def __str__(self):
        return self.document.title


class DocumentAuditActivity(models.Model):
    """
    This model is for stacking document audit activity
    """

    document_submission_activity = models.ForeignKey(DocumentSubmissionActivity)
    result = models.CharField(max_length=15, choices=[
        ("APPROVED", _("Approved")),
        ("DECLINED", _("Declined")),
        ("CANCELED", _("Canceled"))
    ])
    auditor = models.ForeignKey('people.Profile')
    comment_subject = models.CharField(max_length=300,
                                       help_text=_('Comment type to approve or deny layer submission '))
    comment_body = models.TextField(help_text=_('Comments when auditor denied or approved layer submission'),
                               blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


signals.pre_save.connect(pre_save_document, sender=Document)
signals.post_save.connect(create_thumbnail, sender=Document)
signals.post_save.connect(post_save_document, sender=Document)
signals.post_save.connect(resourcebase_post_save, sender=Document)
signals.pre_delete.connect(pre_delete_document, sender=Document)
map_changed_signal.connect(update_documents_extent)
#end