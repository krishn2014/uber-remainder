# apiapp
from django.conf.urls import patterns, include, url
# for including static content
import imp, os.path

from views import *

# @deprecated
# from django.views.generic.simple import direct_to_template
from django.shortcuts import render as direct_to_template

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mainapp.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # docs url
    url(r'^$',root_page),
)

# Django REST framework
from rest_framework import routers

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.
urlpatterns += patterns('',

    url(r'^form/$', post_new, name='post_new'),
    # url(r'^post/new/$', views.post_new, name='post_new'),
)
