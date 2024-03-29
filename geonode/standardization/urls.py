from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from geonode.news.views import NewsList, NewsCreate, NewsUpdate, NewsDelete, NewsDetails
from geonode.standardization.views import DPSListView, DPSCreateView


urlpatterns = patterns(
    'geonode.news.views',

    url(r'^projection/?$', TemplateView.as_view(template_name='projection.html'), name='projection'),
    url(r'^nsdi-policy/?$', TemplateView.as_view(template_name='nsdi_policy_new.html'), name='nsdi-policy'),
    url(r'^data-product-specification/?$', TemplateView.as_view(template_name='dps.html'), name='nsdi-dps'),

    url(r'^data-product-specification-list/?$',DPSListView.as_view(), name='nsdi-dps-list'),
    url(r'^data-product-specification-create/?$',DPSCreateView.as_view(), name='nsdi-dps-create'),

)