from django.conf.urls import include, url
from cognitive.apps.main import urls as main_urls
from cognitive.apps.users import urls as users_urls

urlpatterns = [ url(r'^', include(main_urls)),
                url(r'^accounts/', include(users_urls))
]
