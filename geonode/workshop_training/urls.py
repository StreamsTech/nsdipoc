from django.conf.urls import patterns, url
from django.views.generic import TemplateView


from geonode.workshop_training.views import WorkshopTrainingListView, WorkshopTrainingDetailsView, WorkshopTrainingCreateView
from geonode.workshop_training.views import WorkshopTrainingDocumentCreateView, WorkshopTrainingDocumentDetailsView, WorkshopTrainingDocumentEditView


urlpatterns = patterns(
    'geonode.workshop_training.views',

    url(r'^workshop-training-list/?$',WorkshopTrainingListView.as_view(), name='workshop-training-list'),
    url(r'^workshop-training-create/?$',WorkshopTrainingCreateView.as_view(), name='workshop-training-create'),
    url(r'^(?P<workshop_pk>[0-9]+)/document-create/?$',WorkshopTrainingDocumentCreateView.as_view(), name='workshop-training-document-create'),
    url(r'^(?P<workshop_pk>[0-9]+)/details$', WorkshopTrainingDetailsView.as_view(), name='workshop-training-details'),
    url(r'^(?P<workshop_pk>[0-9]+)/document/(?P<document_pk>[0-9]+)/details$', WorkshopTrainingDocumentDetailsView.as_view(), name='workshop-training-document-details'),
    url(r'^(?P<workshop_pk>[0-9]+)/document/(?P<document_pk>[0-9]+)/edit$', WorkshopTrainingDocumentEditView.as_view(), name='workshop-training-document-edit'),
    # url(r'^data-product-specification-create/?$',DPSCreateView.as_view(), name='nsdi-dps-create'),

)