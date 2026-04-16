from django.urls import path, include
 
urlpatterns = [  
    path('accounts/', include('apps.accounts.urls', namespace='accounts')),
    path('rbac/', include('apps.rbac.urls', namespace='rbac')),
    path('students/', include('apps.student.urls', namespace='students')),
    path('courses/', include('apps.course.urls', namespace='courses')),
]


