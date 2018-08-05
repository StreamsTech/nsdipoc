from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator

# Create your models here.

phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                             message="Phone number must be entered in the format: '+8801xxxxxxxxx'. Up to 13 digits allowed.")


class UserFeedback(models.Model):
    """
    This model is for managing user feedback. Users can give
     feedback and super admin will investicate these.
    """

    title = models.CharField(
        verbose_name=_("title"),
        max_length=50,
        # null=False, CHAR and TEXT types are never saved as NULL by Django, so null=True is unnecessary.
        blank=False,
        help_text=_("give a title of your feedback")
    )
    commenter_name = models.CharField(
        verbose_name=_("your name"),
        max_length=200,
        # null=False, CHAR and TEXT types are never saved as NULL by Django, so null=True is unnecessary.
        blank=False,
        help_text=_("")
    )
    commenter_email = models.EmailField(
        verbose_name=_('email'),
        blank=False,
        null=False,
        help_text=_("your email"))
    message = models.TextField(
        verbose_name=_("message"),
        max_length=5000,
        blank=False,
        # null=False, CHAR and TEXT types are never saved as NULL by Django, so null=True is unnecessary.
        help_text=_("write your feedback here"))
    slug = models.SlugField(
        max_length=100,
        null=True,
        blank=True)
    is_active = models.BooleanField(default=True)
    contact_no = models.CharField(
        verbose_name=_("phone"),
        validators=[phone_regex],
        max_length=17,
        blank=False)  # validators should be a list
    attachment = models.FileField(
        verbose_name=_("attachment"),
        blank=True,
        null=True,
        help_text=_("attatch files or documents if any"))
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.title
