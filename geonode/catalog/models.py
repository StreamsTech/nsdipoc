from django.db import models
from django.utils.translation import ugettext_lazy as _
from geonode.groups.models import GroupProfile
# Create your models here.


VALID_FORMAT_CHOICES = (
    ('shape', _('Shape')),
    ('img', _('Imgage')),
    ('arcinfo', _('Arcingo Cov')),
    ('geodatabase', _('ESRI geodatabase, pdf')),
    ('pdf', _('Pdf')),
    ('gcm', _('GCM/GCR, pdf')),
    ('xslx', _('XLSX')),
    ('txt', _('Text')),
    ('netcdf', _('Netcdf')),
    ('scanned', _('Scanned Copy')),
)

COORDINATE_SYSTEM_CHOICES = (
    ('wgs84', _('WGS 84')),
    ('butm', _('BUTM')),
    ('butm2010', _('BUTM 2010')),
    ('projected', _('Projected')),
    ('no', _('N/A')),
    ('gcm', _('GCM/GCR, pdf')),
    ('xslx', _('XLSX')),
    ('txt', _('Text')),
    ('netcdf', _('Netcdf')),
    ('scanned', _('Scanned Copy')),
)




class DataCatalog(models.Model):
    """
    This model is for managing data catalog.
    """

    title = models.CharField(
        verbose_name=_("title"),
        max_length=300,
        # null=False, CHAR and TEXT types are never saved as NULL by Django, so null=True is unnecessary.
        blank=False,
        help_text=_("give a title of your catalog")
    )
    ownership = models.ForeignKey(
        GroupProfile,
        verbose_name=_("owner ship"),
        blank=False,
        null=False,
        help_text=_('the organization that owns this catalog'))
    format = models.CharField(
        _('format of data'),
        max_length=300,
        blank=True,
        help_text=_("type of data, it may Shape, image, pdf etc."))
    no_of_layer = models.CharField(
        _('number of layers'),
        max_length=300,
        blank=True,
        help_text=_("total number of layers"))
    coordinate_system = models.CharField(
        _('coordinate system'),
        max_length=300,
        blank=True,
        help_text=_("the coordinate system of this data"))
    projection = models.CharField(
        _('projection'),
        max_length=300,
        blank=True,
        help_text=_("projection of data"))
    dimension = models.CharField(
        _('dimension (2D/3D)'),
        max_length=300,
        blank=True,
        help_text=_("dimension (2D/3D with height)"))
    display_scale = models.CharField(
        _('display scale'),
        max_length=300,
        blank=True,
        help_text=_("suitable scale for dispalay"))
    area = models.CharField(
        _('area covered'),
        max_length=300,
        blank=True,
        help_text=_("total area covered by the layers"))
    preparation_year = models.CharField(
        _('year of preparation'),
        max_length=300,
        blank=True,
        help_text=_("year of preparation/revision"))
    volume = models.CharField(
        _('volume'),
        max_length=300,
        blank=True,
        help_text=_("volume of data (KB, MB, GB)"))
    govt_org = models.CharField(
        _('governmental organization only'),
        max_length=300,
        blank=True,
        help_text=_("governmental organization only"))
    inside_ministy = models.CharField(
        _('inside the ministry'),
        max_length=300,
        blank=True,
        help_text=_("inside the ministry only"))
    inside_org = models.CharField(
        _('inside the organization'),
        max_length=300,
        blank=True,
        help_text=_("inside the organization only"))
    restricted_information = models.CharField(
        _('restricted information'),
        max_length=300,
        blank=True,
        help_text=_("total restricted information"))
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.title
