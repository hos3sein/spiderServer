from django.urls import path

from . import views


urlpatterns = [
    path("", views.no, name="no"),
    path("test/", views.index, name="index"),
    # path("test2/", views.test, name="test"),
    path("getAllData/", views.getAllData, name="getData"),
    # path("get/", views.test, name="test"),
    # path("getSpecificCoin/", views.test, name="test"),
    # path("get/", views.test, name="test"),
]