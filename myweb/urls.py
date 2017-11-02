"""myweb URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from blog.models import *
admin.site.register([Catagory,Tag,Blog,Book,Movie])
from blog.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.views import static


from . import view

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', index, name='homepage'),
    url(r'^blogs/$', get_blogs, name='get_blogs'),
    url(r'^login/$', login, name='login'),
    url(r'^signup/$', signup, name='signup'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^add_book/$', add_book, name='add_book'),
    url(r'^view_book/detail/$', detail, name='detail'),
    url(r'^add_img/$', add_img, name='add_img'),
    url(r'^set_password/$', set_password, name='set_password'),
    url(r'^blist/$', view_blog_list, name='view_blog_list'),
    url(r'^books/$', view_book_list, name='view_book_list'),
    url(r'^detail/(\d+)/$', get_details, name='blog_get_detail'),
    url(r'^movie/$', movie, name='movie'),
    url(r'^catagory/(\d+)/$', get_catagory_detail, name='catagory_get_detail'),
    # url(r'^media/(?P<path>.*)$', static., {'document_root': settings.MEDIA_ROOT}, name="media")
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^static/(?P<path>.*)$', static.serve, {'document_root': settings.STATIC_ROOT}, name="static"),
        url(r'^media/(?P<path>.*)$', static.serve, {'document_root': settings.MEDIA_ROOT}, name="media")
    ]
