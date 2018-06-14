from django.conf.urls import patterns, url

from geonode.nsdi import views

urlpatterns = patterns('',
  url(r'^sector/list$', views.SectorList.as_view(), name='sector_list'),
  url(r'^sector/add$', views.SectorCreate.as_view(), name='sector_new'),
  url(r'^sector/edit/(?P<sector_pk>\d+)$', views.SectorUpdate.as_view(), name='sector_edit'),
  url(r'^sector/delete/(?P<sector_pk>\d+)$', views.SectorDelete.as_view(), name='sector_delete'),

  url(r'^type/list$', views.DepartmentList.as_view(), name='department_list'),
  url(r'^type/add$', views.DepartmentCreate.as_view(), name='department_new'),
  url(r'^type/edit/(?P<department_pk>\d+)$', views.DepartmentUpdate.as_view(), name='department_edit'),
  url(r'^type/delete/(?P<department_pk>\d+)$', views.DepartmentDelete.as_view(), name='department_delete'),
)