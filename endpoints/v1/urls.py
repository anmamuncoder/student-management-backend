from django.urls import path, include
 
urlpatterns = [  
    path('accounts/', include('apps.accounts.urls', namespace='accounts')),
    path('rbac/', include('apps.rbac.urls', namespace='rbac')),

]


