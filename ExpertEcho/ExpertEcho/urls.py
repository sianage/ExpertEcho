from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Homepage.urls')),
    path('blogs/', include('Blogs.urls')),
    path('members/', include('django.contrib.auth.urls')),
    path('members/', include('Members.urls')),
    path('poll/', include('Polls.urls')),
    path('debates/', include('Debates.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)