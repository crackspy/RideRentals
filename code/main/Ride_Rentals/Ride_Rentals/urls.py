from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('mainapp.urls'))
]


if settings.DEBUG: # Only do this in development! For production, configure your web server
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
