
from django.conf.urls import url

from list_search_apis import ResourceBaseListSearchAPIView


#api urls for layers list and layer search
urlpatterns = [
    url(r'^resources-list$', ResourceBaseListSearchAPIView.as_view(), name='rsources-list-search-api')
]