from django.conf.urls import url,patterns

from . import api_views, views


urlpatterns = [
    url(r'^concepts$', views.all_concepts, name="all_concepts"),
    url(r'^concepts/(?P<letter>[a-z]|[A-Z]{1})/$', views.concepts_by_letter, 
        name="concepts_by_letter"),
]

api_urls = [
    url(r'^api/search$', api_views.SearchAPI.as_view(), name='task_api_list'),
    url(r'^api/concept$',api_views.ConceptAPI.as_view(), name='task_api_list'),
    url(r'^api/task$', api_views.TaskAPI.as_view(), name='task_api_list'),
    url(r'^api/disorder', api_views.DisorderAPI.as_view(), name='task_api_list'),
]

urlpatterns += api_urls
