from django.conf.urls import url,patterns

from . import views
from .api_views import TaskAPIList


urlpatterns = [
    url(r'^concepts$', views.all_concepts, name="all_concepts"),
    url(r'^concepts/(?P<letter>[a-z]|[A-Z]{1})/$', views.concepts_by_letter, 
        name="concepts_by_letter"),
    url(r'^api/$', TaskAPIList.as_view(), name='task_api_list'),
]

