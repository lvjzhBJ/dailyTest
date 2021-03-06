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
    url(r'^(?P<un>.*)/(?P<pjt>.*)/report/flow/$', views.rpt_flow),
    url(r'^(?P<un>.*)/(?P<pjt>.*)/report/sum/$', views.rpt_sum),
    url(r'^(?P<un>.*)/(?P<pjt>.*)/report/fcs/$', views.rpt_function),
    url(r'^(?P<un>.*)/(?P<pjt>.*)/report/manual/$', views.rpt_manual),
    url(r'^(?P<un>.*)/(?P<pjt>.*)/show/$', views.pjt_show),
    url(r'^(?P<un>.*)/(?P<pjt>.*)/edit/$', views.pjt_edit),
    url(r'^(?P<un>.*)/(?P<pjt>.*)/case/$', views.pjt_case),
    url(r'^(?P<un>.*)/(?P<pjt>.*)/manage/$', views.pjt_manage),
    url(r'^(?P<un>.*)/(?P<pjt>.*)/delc/(?P<cn>.*)/$', views.del_case),
    url(r'^(?P<un>.*)/(?P<pjt>.*)/fcs/$', views.pjt_func),
    url(r'^(?P<un>.*)/show/$', views.user_show),
    url(r'^(?P<un>.*)/pjt2stand/$', views.pjt2stand),
    url(r'^(?P<un>.*)/apk2oss/$', views.apk2oss),
    url(r'^get_oss_token/$', views.get_oss_token),
    url(r'^pjt2db/$', views.pjtinfo2db),
    url(r'^(?P<un>.*)/pross/$', views.user_pross),
    url(r'^(?P<un>.*)/del/$', views.user_del),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
