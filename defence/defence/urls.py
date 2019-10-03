"""defence URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf.urls import url, include
from rest_framework import routers, serializers, viewsets
from sample.models import registration,User,app
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.authtoken import views
from rest_framework.documentation import include_docs_urls


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email']
class registrationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model= registration
        fields = ['firmname', 'firmhead', 'username','email','password']
class appSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model= app
        fields = ['url', 'app_name', 'role_id']


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class registrationViewSet(viewsets.ModelViewSet):
    queryset = registration.objects.all()
    serializer_class = registrationSerializer
    
class appViewSet(viewsets.ModelViewSet):
    queryset = app.objects.all()
    serializer_class = appSerializer

class appListView(viewsets.ModelViewSet):
    queryset = app.objects.all()
    serializer_class = appSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('app_name', 'role_id')

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'registration', registrationViewSet)
router.register(r'app', appViewSet)
router.register(r'app_filter', appListView)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('sample.urls')),
    url(r'^', include(router.urls)),
    url('api/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^get_token/', views.obtain_auth_token, name='get_token'),
    path(r'docs/', include_docs_urls(title="DRDO APIs", urlconf='defence.urls'))
]
