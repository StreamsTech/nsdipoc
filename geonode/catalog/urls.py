from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from views import DataCatalogList, DataCatalogCreate, DataCatalogUpdate, DataCatalogDelete, CatDownloadRequest

urlpatterns = patterns(
    'geonode.feedback.views',

    # home page section management with image and texts
    url(r'^list/(?P<org>[-\w]+)/$', DataCatalogList.as_view(), name='data_catalog_list'),
    url(r'^create$', DataCatalogCreate.as_view(), name='data_catalog_create'),

    url(r'^edit/(?P<cat_pk>\d+)$', DataCatalogUpdate.as_view(), name='data_catalog_edit'),
    url(r'^delete/(?P<cat_pk>\d+)$', DataCatalogDelete.as_view(), name='data_catalog_delete'),

    url(r'^download/request/(?P<org>[-\w]+)/$', CatDownloadRequest.as_view(), name='download_cat_request'),

)
