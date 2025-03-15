
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('base/', include('base.urls')),
    path('blog/', include('blog.urls')),

    path('tinymce/', include('tinymce.urls')), 
    
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]+ debug_toolbar_urls()
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

