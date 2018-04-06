"""decast_eirc URL Configuration

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
from django.conf.urls import url, include
from django.contrib import admin

from rest_framework.urlpatterns import format_suffix_patterns
from devices import views

# removable block
from rest_framework_jwt.views import refresh_jwt_token
from rest_framework_jwt.views import verify_jwt_token
from rest_framework_jwt.views import obtain_jwt_token

authorization_urls = [
  url(r'^api-token-auth/', obtain_jwt_token),
  url(r'^api-token-refresh/', refresh_jwt_token),
  url(r'^api-token-verify/', verify_jwt_token),
  ]
# removable block end

eirc_devices_urls = [
    url(r'^$', views.EIRCDeviceList.as_view()),
    url(r'^(?P<id>[0-9]+)/$', views.EIRCDeviceDetail.as_view()),
    url(r'^(?P<id>[0-9]+)/change_reading/$', views.EIRCChangeReading.as_view()),
  ]
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^eirc_devices/', include(eirc_devices_urls)),
    url(r'^eirc_device/', views.EIRCDeviceByAccount.as_view()),
    url(r'^auth/', include(authorization_urls)),
]

urlpatterns = format_suffix_patterns(urlpatterns)
