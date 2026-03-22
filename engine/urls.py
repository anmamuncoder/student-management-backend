import django
from django.contrib import admin
from django.urls import include, path

from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    return render(request, 'index.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    
    # API endpoints
    path('api/v1/', include('endpoints.v1.urls')),
]
