"""mobile_backend URL Configuration

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
from devices import views as devices_views

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

devices_urls = [
    url(r'^$', devices_views.DeviceList.as_view()),
    url(r'^(?P<id>[0-9]+)/$', devices_views.DeviceDetail.as_view()),
    url(r'^(?P<id>[0-9]+)/readings/$', devices_views.DeviceReadings.as_view()),
    url(r'^(?P<id>[0-9]+)/readings/(?P<rid>[0-9]+)/$', devices_views.ReadingDetail.as_view()),
  ]

user_urls = [
    url(r'^$', devices_views.UserByEmail.as_view()),
  ]

users_urls = [
    url(r'^$', devices_views.UsersByEmail.as_view()),
    url(r'^(?P<id>[0-9]+)/devices/$', devices_views.DevicesByUserId.as_view()),
  ]

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^devices/',include(devices_urls)),
    url(r'^user/',include(user_urls)),
    url(r'^users/',include(users_urls)),
    # the string below is removable
    url(r'^auth/',include(authorization_urls)),
    #url(r'^user/$', devices_views.UserByEmail.as_view()),
    #url(r'^devices/$', devices_views.DeviceList.as_view()),
   # url(r'^devices/(?P<id>[0-9]+)/$', devices_views.DeviceDetail.as_view()),
   # url(r'^users/(?P<id>[0-9]+)/devices/$', devices_views.DevicesByUserId.as_view()),
   # url(r'^devices/(?P<id>[0-9]+)/readings$', devices_views.DeviceReadings.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
