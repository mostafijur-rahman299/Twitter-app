# @Date:   2019-01-07T00:33:38+06:00
# @Last modified time: 2019-03-13T04:06:15+06:00
"""twitter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path,include

from django.conf import settings
from django.conf.urls.static import static
from tweets.views import TweetListView
from .views import SearchView

urlpatterns = [
    path('',TweetListView.as_view(),name='tweet_list'),
    path('admin/', admin.site.urls),
    path('tweets/',include('tweets.urls')),
    path('api/',include('tweets.api.urls')),
    path('accounts/',include('accounts.urls')),
    path('account/',include('accounts.password.urls')),
    path('tags/',include('hashtags.urls')),
    path('api/',include('accounts.api.urls')),
    path('/',SearchView.as_view(),name='search')
]

if settings.DEBUG:
    urlpatterns += \
                static(settings.STATIC_URL,document_root = settings.STATIC_ROOT)
    urlpatterns += \
                static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
