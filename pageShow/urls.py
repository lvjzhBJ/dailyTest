"""dailyTest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^del_pjt/(?P<pjt>.*)/$', views.del_pjt),
    url(r'^(?P<un>.*)/(?P<pjt>.*)/report/show/$', views.rpt_show),
    url(r'^(?P<un>.*)/(?P<pjt>.*)/report/sum/$', views.rpt_sum),
    url(r'^(?P<un>.*)/(?P<pjt>.*)/report/playback/$', views.rpt_playback),
    url(r'^(?P<un>.*)/(?P<pjt>.*)/show/$', views.pjt_show),
    url(r'^(?P<un>.*)/(?P<pjt>.*)/edit/$', views.pjt_edit),
    url(r'^(?P<un>.*)/(?P<pjt>.*)/case/$', views.pjt_case),
    url(r'^(?P<un>.*)/show/$', views.user_show),
    url(r'^(?P<un>.*)/add/$', views.user_add),
    url(r'^(?P<un>.*)/new/$', views.user_new),
    url(r'^(?P<un>.*)/del/$', views.user_del),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
