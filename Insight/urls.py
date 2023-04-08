from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from core import urls as coreUrls

from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(coreUrls)),
    # path('', lambda request: redirect('/api'))
]

urlpatterns += static(
                settings.MEDIA_URL,
                document_root = settings.MEDIA_ROOT
            )

urlpatterns += static(
                settings.STATIC_URL,
                document_root = settings.STATIC_ROOT
            )
        
