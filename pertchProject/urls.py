from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pet/', include('petApp.urls')),
    path('owner/', include('ownerApp.urls')),
    path('petComment/', include('petCommentApp.urls'))
] + static(settings.STATIC_URL, document_root = settings.STATIC_ROOT) \
+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)