from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    path('api/', include('movies.api.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    urlpatterns += [
        path('debug/', include('debug_toolbar.urls')),
    ]
