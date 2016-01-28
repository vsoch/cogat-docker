from django.conf.urls import url,patterns
from . import views

urlpatterns = [
    url(r'^concepts$', views.all_concepts, name="all_concepts"),
    url(r'^concepts/(?P<letter>[A-Z]{1})/$', views.concepts_by_letter, name="concepts_by_letter")
]

