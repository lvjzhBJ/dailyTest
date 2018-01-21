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
    url(r'^del_pjt/(\S+)/$', views.del_pjt),
    url(r'^(\S+)/(\S+)/report/show/$', views.rpt_show),
    url(r'^(\S+)/(\S+)/report/sum/$', views.rpt_sum),
    url(r'^(\S+)/(\S+)/report/playback/$', views.rpt_playback),
    url(r'^(\S+)/(\S+)/show/$', views.pjt_show),
    url(r'^(\S+)/(\S+)/edit/$', views.pjt_edit),
    url(r'^(\S+)/(\S+)/case/$', views.pjt_case),
    url(r'^(\S+)/show/$', views.user_show),
    url(r'^(\S+)/add/$', views.user_add),
    url(r'^(\S+)/del/$', views.user_del),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
