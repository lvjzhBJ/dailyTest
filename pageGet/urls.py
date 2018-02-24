from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^p2c/$', views.pjt2client),
    url(r'^c2j/$', views.client2json),
    url(r'^c2i/$', views.client2img),
]
