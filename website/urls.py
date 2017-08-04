from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^mlearn/', include('mlearn.urls')),
    # url(r'^media/(?P<file_name>[0-9a-zA-Z._]+)$', views.getfile, name='getfile'),
    # url(r'^media/train_(?P<competition_id>[0-9]+).txt$', views.getfile, name='gettrain'),
    url(r'^', include('mlearn.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
