Create project

Create app

Create models in models.py 

In app folder create subfolder api

### app/api/serializers.py
from rest_framework import serializers
from app.models import appModel

class appSerializer(serializers.ModelSerializer):
    class Meta:
        model = appModel
        fields = ('a', 'b', 'c') # field names to display
        fields = '__all__' # displays all field names

### app/api/viewsets.py
from app.models import appModel 
from .serializers import appSerializer
from rest_framework import viewsets

class appViewSet(viewsets.ModelViewSet):
    queryset = appModel.objects.all()
    serializer_class = appSerializer

### project/router.py
from app.api.viewsets import appViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('app', appViewSet)

### project/urls.py
from django.urls import path, include
from .router import router

path('api/', include(router.urls)), # include to urls list

### runserver 
api for app is located at http://localhost:8000/api/app also /id to update/delete ?format=json

### adding decorators to app/api/viewsets.py
from rest_framework.decorators import action
from rest_framework.response import Response

// add chunk to appViewSet
@action(methods = ['get'], detail = False)
    def newest(self, request):
        newest = self.get_queryset().order_by('created').last()
        serializer = self.get_serializer_class()(newest)
        return Response(serializer.data)

### authentication preliminaries
In project/settings.py, create a new dictionary REST_FRAMEWORK

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES' : (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES' : (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

After adding these, a get request returns a 401 forbidden with the following headers because no Token was provided

Date →Tue, 23 Apr 2019 20:58:52 GMT
Server →WSGIServer/0.2 CPython/3.7.3
Content-Type →application/json
WWW-Authenticate →Token
Vary →Accept
Allow →GET, POST, HEAD, OPTIONS
X-Frame-Options →SAMEORIGIN
Content-Length →58


To project/urls.py add

from rest_framework.authtoken import views

path('api-token-auth/', views.obtain_auth_token, name = 'api-token-auth')

To installed apps, include 'rest_framework.authtoken'

### createsuperuser & migrate

You have to migrate after because with the auth.token you have a new model

### request new token

Make a POST request and get a token that can be used 
using httpie, 

`pip install httpie`

`http POST http://localhost:8000/api-auth-token/ username="username" password="password"`

returns 

{
    'token': '550506729cbd8303774884aedeafe626e55f9fa1'
}

repeating the request returns the same token so one token per superuser

### Making a GET request with token

`http GET http://localhost:8000/api/snippets/ "Authorization: Token 550506729cbd8303774884aedeafe626e55f9fa1"`

returns the data available at the url 

### Using session auth
In project/settings.py, edit dictionary REST_FRAMEWORK

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES' : (
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES' : (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

changing TokenAuthentication to SessionAuthentication

Then in project/urls.py,
from django.contrib.auth.views import login

path('login/', views.login, name = 'login')

... check this out

### permissions & authentication alternatives
In app/api/viewsets.py import classes and include in appViewSet

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

within the class, 
authentication_classes = (TokenAuthentication,)
permission_classes = (IsAuthenticated,)

### filtering
install django-filter
add 'django_filters' to installed apps in project/settings.py and a new dictonary REST_FRAMEWORK...

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',)
}

This sets the default filters for every user. Alternatively, to the appViewSet add `filter_backends = (DjangoFilterBackend,)` and `from django_filters.rest_framework import DjangoFilterBackend`

from django_filters import rest_framework as filters 

class SnippetFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr = 'icontains')
    class Meta:
        model = Snippet
        fields = ('title',)

class SnippetFilter2(filters.FilterSet):
    class Meta:
        model = Snippet
        fields = {
            'id': ['lte', 'gte'],
            'title': ['icontains'],
            'created': ['iexact', 'lte', 'gte']
        }

where lte & gte are less than or equal to and greater than or equal to respectively