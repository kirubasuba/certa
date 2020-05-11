from django.contrib import admin
from django.urls import re_path

from . import views

urlpatterns = [
    re_path(r'^login/$', views.login, name="login"),
    re_path(r'^logout/$', views.logout, name="logout"),
    re_path(r'^password-reset/$', views.forgotPassword, name="password-reset"),
    re_path(r'^enroll/$', views.register, name="enroll"),
    re_path(r'^sign_up/$', views.sign_up, name="sign_up")
]
