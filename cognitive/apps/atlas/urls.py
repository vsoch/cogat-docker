from django.conf.urls import url,patterns

from . import api_views, views


urlpatterns = [
    url(r'^concepts$', views.all_concepts, name="all_concepts"),
    url(r'^disorders$', views.all_disorders, name="all_disorders"),
    url(r'^concepts/(?P<letter>[a-z]|[A-Z]{1})/$', views.concepts_by_letter, name="concepts_by_letter"),
    url(r'^tasks/(?P<letter>[a-z]|[A-Z]{1})/$', views.tasks_by_letter, name="tasks_by_letter"),
    url(r'^disorder/(?P<did>[a-z]|[A-Z]{1})/$', views.view_disorder, name="disorder"),

]

api_urls = [
    url(r'^api/search$', api_views.SearchAPI.as_view(), name='task_api_list'),
    url(r'^api/concept$',api_views.ConceptAPI.as_view(), name='task_api_list'),
    url(r'^api/task$', api_views.TaskAPI.as_view(), name='task_api_list'),
    url(r'^api/disorder', api_views.DisorderAPI.as_view(), name='task_api_list'),
]

urlpatterns += api_urls
