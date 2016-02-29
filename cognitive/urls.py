from django.conf.urls import include, url, patterns
from django.conf.urls.static import static
from cognitive.apps.main import urls as main_urls
from cognitive.apps.users import urls as users_urls
from cognitive.apps.atlas import urls as atlas_urls
import cognitive.settings as settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [ url(r'^', include(main_urls)),
                url(r'^', include(atlas_urls)),
                url(r'^accounts/', include(users_urls))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
