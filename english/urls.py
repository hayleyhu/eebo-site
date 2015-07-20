"""eebo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from english import views
from english.views import findentry
admin.autodiscover()
urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^admin/', include(admin.site.urls)),


    url(r'^lookup/$', 'english.views.lookup'),
    url(r'^$', findentry),
    url(r'^findentry/$', 'english.views.findentry'),
    url(r'^wordinfo/(?P<pk>[0-9]+)/$', 'english.views.wordinfo'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^requesttoedit/$', views.requesttoedit, name='requesttoedit'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^revision/$', 'english.views.revision'),
]
