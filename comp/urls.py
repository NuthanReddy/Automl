from django.conf.urls import url

from . import views

app_name = 'comp'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<competition_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<competition_id>[0-9]+)/data$', views.data, name='data'),
    url(r'^(?P<competition_id>[0-9]+)/score$', views.score, name='score'),
    url(r'^(?P<competition_id>[0-9]+)/submit$', views.submit, name='submit'),
]