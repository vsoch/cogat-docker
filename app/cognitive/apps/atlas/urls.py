from django.conf.urls import url,patterns
from . import views

urlpatterns = [
    url(r'^concepts$', views.all_concepts, name="all_concepts"),
    url(r'^disorders$', views.all_disorders, name="all_disorders"),
    url(r'^concepts/(?P<letter>[a-z]|[A-Z]{1})/$', views.concepts_by_letter, name="concepts_by_letter"),
    url(r'^tasks/(?P<letter>[a-z]|[A-Z]{1})/$', views.tasks_by_letter, name="tasks_by_letter"),
    url(r'^disorder/(?P<did>[a-z]|[A-Z]{1})/$', views.view_disorder, name="disorder"),

]

