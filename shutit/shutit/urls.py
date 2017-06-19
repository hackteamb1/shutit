"""shutit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'queue', views.QueueViewSet)

urlpatterns = [
    url(r'^api/state/(?P<passenger_id>[0-9]+)$', views.passenger_state),
    url(r'^$', views.index_view, name="index"),
    url(r'^api/', include(router.urls)),
    url(r'^login$', views.login_view, name="login"),
    url(r'^signup$', views.signup_view, name="signup"),
    url(r'^admin/', admin.site.urls),
]
