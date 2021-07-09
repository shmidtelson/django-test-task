"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from auction.views import UserViewSet, BetViewSet, LotViewSet, ItemViewSet

# Routers provide an easy way of automatically determining the URL conf.
from core.settings import API_PREFIX

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'bets', BetViewSet)
router.register(r'lots', LotViewSet)
router.register(r'items', ItemViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path(API_PREFIX, include(router.urls)),
    path(f'{API_PREFIX}auth/', include('rest_framework.urls'))
]
