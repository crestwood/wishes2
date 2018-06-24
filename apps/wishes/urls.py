from django.conf.urls import url
from . import views           
urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^dashboard$', views.dashboard),
    url(r'^logout$', views.logout),
    url(r'^additempage$', views.additempage),
    url(r'^createItem$', views.createItem),
    url(r'^view_item/(?P<id>\d+)$', views.viewItem),
    url(r'^delete$', views.delete),
    url(r'^like$', views.like),
    url(r'^remove$', views.remove),
]