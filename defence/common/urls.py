from django.contrib import admin
from django.urls import path, include, re_path
from authmgmt import views as auth_views
from dashboard import views as dashboard_views

from . import views

urlpatterns = [
    re_path(r'^$', dashboard_views.dashboard, name="home"),
    re_path(r'^auth/', include('authmgmt.urls')),
    re_path(r'^dashboard/', include('dashboard.urls'))
]

