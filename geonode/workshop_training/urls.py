from django.conf.urls import patterns, url
from django.views.generic import TemplateView


from geonode.workshop_training.views import WorkshopTrainingListView, WorkshopTrainingDetailsView


urlpatterns = patterns(
    'geonode.workshop_training.views',

    url(r'^workshop-training-list/?$',WorkshopTrainingListView.as_view(), name='workshop-training-list'),
    url(r'^(?P<workshop_pk>[0-9]+)/details$', WorkshopTrainingDetailsView.as_view(), name='workshop-training-details'),
    # url(r'^data-product-specification-create/?$',DPSCreateView.as_view(), name='nsdi-dps-create'),

)