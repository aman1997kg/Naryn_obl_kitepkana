from django.contrib import admin
from django.views.static import serve

from django.urls import path, include
from django.conf.urls.static import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('nok_web.urls')),
    path('accounts/', include('django.contrib.auth.urls')),

    #path('media/<path>', serve, {'document_root': settings.MEDIA_ROOT}),
    #path('static/<path>', serve, {'document_root': settings.STATIC_ROOT}),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)