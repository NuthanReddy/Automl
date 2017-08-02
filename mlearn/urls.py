from django.conf.urls import url
from . import views

app_name = 'mlearn'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    #url(r'^(?P<competition_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<competition_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^add_dataset/$', views.create_dataset, name='create_dataset'),
    url(r'^(?P<dataset_id>[0-9]+)/delete_dataset/$', views.delete_dataset, name='delete_dataset'),
]
