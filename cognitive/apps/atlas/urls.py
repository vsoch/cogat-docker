from django.conf.urls import url,patterns
from django.conf.urls.static import static

from . import api_views, views, graph


urlpatterns = [

    # All views
    url(r'^concepts$', views.all_concepts, name="all_concepts"),
    url(r'^disorders$', views.all_disorders, name="all_disorders"),
    url(r'^batteries$', views.all_batteries, name="all_batteries"),
    url(r'^theories$', views.all_theories, name="all_theories"),
    url(r'^tasks$', views.all_tasks, name="all_tasks"),

    # Search (json response) views
    url(r'^search$', views.search_all, name="search"), # GET for json response
    url(r'^concepts/search$', views.search_concept, name="search_concept"),

    # View by letter
    url(r'^concepts/(?P<letter>[a-z]|[A-Z]{1})/$', views.concepts_by_letter, name="concepts_by_letter"),
    url(r'^tasks/(?P<letter>[a-z]|[A-Z]{1})/$', views.tasks_by_letter, name="tasks_by_letter"),

    # Single View
    url(r'^disorder/id/(?P<uid>[\w\+%_& ]+)/$', views.view_disorder, name="disorder"),
    url(r'^battery/id/(?P<uid>[\w\+%_& ]+)/$', views.view_battery, name="battery"),
    url(r'^theory/id/(?P<uid>[\w\+%_& ]+)/$', views.view_theory, name="theory"),
    url(r'^concept/id/(?P<uid>[\w\+%_& ]+)/$', views.view_concept, name="concept"),
    url(r'^task/id/(?P<uid>[\w\+%_& ]+)/$', views.view_task, name="task"),
    url(r'^contrast/id/(?P<uid>[\w\+%_& ]+)/$', views.view_contrast, name="contrast"),

    # Modify terms
    url(r'^terms/new/$', views.contribute_term, name="contribute_term"),
    url(r'^terms/add/$', views.add_term, name="add_term"),
    url(r'^concept/update/(?P<uid>[\w\+%_& ]+)/$', views.update_concept, name="update_concept"),
    url(r'^task/update/(?P<uid>[\w\+%_& ]+)/$', views.update_task, name="update_task"),
    url(r'^disorder/update/(?P<uid>[\w\+%_& ]+)/$', views.update_disorder, name="update_disorder"),
    url(r'^theory/update/(?P<uid>[\w\+%_& ]+)/$', views.update_theory, name="update_theory"),
    url(r'^concept/assert/(?P<uid>[\w\+%_& ]+)/$', views.add_concept_relation, name="add_concept_relation"),

    # Graph views
    url(r'^graph/task/(?P<uid>[\w\+%_& ]+)/$', graph.task_graph, name="task_graph"),
    url(r'^graph/concept/(?P<uid>[\w\+%_& ]+)/$', graph.concept_graph, name="concept_graph"),
    url(r'^graph/$', graph.explore_graph, name="explore_graph"),

] 

api_urls = [
    url(r'^api/search$', api_views.SearchAPI.as_view(), name='search_api_list'),
    url(r'^api/concept$',api_views.ConceptAPI.as_view(), name='concept_api_list'),
    url(r'^api/task$', api_views.TaskAPI.as_view(), name='task_api_list'),
    url(r'^api/disorder', api_views.DisorderAPI.as_view(), name='disorder_api_list'),
    url(r'^task/json/(?P<uid>[\w\+%_& ]+)/$', graph.task_json, name="task_json"),
    url(r'^concept/json/(?P<uid>[\w\+%_& ]+)/$', graph.concept_json, name="concept_json"),

]

urlpatterns += api_urls
