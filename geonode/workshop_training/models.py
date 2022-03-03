from django.db import models
from geonode.groups.models import GroupProfile
from geonode.people.models import Profile


DAY_TYPE_SLUGS = (
    ("GENERAL", "General Information"),
    ("DAY1", "Day 1"),
    ("DAY2", "Day 2"),
    ("DAY3", "Day 3"),
    ("DAY4", "Day 4"),
    ("DAY5", "Day 5"),
)


class WorkshopTraining(models.Model):
    """
    This model is for training/course management
    """
    title = models.CharField(max_length=200)
    days = models.IntegerField(verbose_name="Days")
    date_from = models.DateTimeField(verbose_name="Date from")
    date_to = models.DateTimeField(verbose_name="To")
    overview = models.TextField(max_length=300, blank=True, null=True, verbose_name="Overview")
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class WorkshopDay(models.Model):
    type = models.CharField(max_length=200, choices=DAY_TYPE_SLUGS,
                  default="GENERAL")
    training_course = models.ForeignKey(WorkshopTraining, related_name="workshop_days")
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.type


class WorkshopDocument(models.Model):
    user = models.ForeignKey(Profile, related_name="documents")
    organization = models.ForeignKey(GroupProfile, related_name="documents")
    title = models.CharField(max_length=200)
    doc_file = models.FileField(upload_to='workshop_training')
    workshop_day = models.ForeignKey(WorkshopTraining, related_name="documents")
    description = models.TextField(max_length=300, blank=True, null=True, verbose_name="Description")
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
