
from django.conf.urls import url,include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include('userAuth.urls')),
    url(r'', include('pageShow.urls')),
    url(r'', include('pageGet.urls')),
]
