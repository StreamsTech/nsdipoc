from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from geonode.news.views import NewsList, NewsCreate, NewsUpdate, NewsDelete, NewsDetails


urlpatterns = patterns(
    'geonode.news.views',

    url(r'^projection/?$', TemplateView.as_view(template_name='projection.html'), name='projection'),
    url(r'^nsdi-policy/?$', TemplateView.as_view(template_name='nsdi_policy.html'), name='nsdi-policy'),
    url(r'^data-product-specification/?$', TemplateView.as_view(template_name='dps.html'), name='nsdi-dps'),

)