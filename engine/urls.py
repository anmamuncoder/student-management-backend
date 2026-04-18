import django
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import TemplateView

from django.http import HttpResponse
from django.shortcuts import render

from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

# def home(request):
#     return render(request, 'index.html')

class ReactAppView(TemplateView):
    template_name = "index.html"


urlpatterns = [
    path('admin/', admin.site.urls), 
    # path('', home, name='home'),
    
    # API endpoints
    path('api/v1/', include('endpoints.v1.urls')),
] 

# STATIC FILES (Django)
urlpatterns += static(
    settings.STATIC_URL,
    document_root=settings.STATIC_ROOT
)


# FIX: /img/* → /static/*
urlpatterns += [
    re_path(
        r'^img/(?P<path>.*)$',
        serve,
        {'document_root': settings.STATIC_ROOT},
    ),
]


# REACT FALLBACK (LAST)
urlpatterns += [
    re_path(r'^.*$', ReactAppView.as_view()),
]

