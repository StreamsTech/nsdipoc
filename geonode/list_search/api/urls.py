
from django.conf.urls import url

from list_search_apis import LayersListSearchAPIView


#api urls for layers list and layer search
urlpatterns = [
    url(r'^layers-list$', LayersListSearchAPIView.as_view(), name='layers-list-search-api')
]