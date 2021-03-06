from django.conf.urls import url
from . import views

app_name = 'people'

urlpatterns = [
	url(r'^$', views.list, name = 'list'),
	url(r'^edit$', views.edit, name = 'edit'),
	url(r'^(?P<pk>\d+)$', views.profile, name = 'profile')
]
