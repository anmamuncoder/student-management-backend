from django.urls import path, include

from .views import SelfPermissionView
from .routers import router

app_name = "rbac"
urlpatterns = [  
    path('permissions/self/',SelfPermissionView.as_view(),name="rbac-self-permissions"),

    # Router endpoints
    path('', include(router.urls)),
]

# Final URL pattern:
# /api/view/rbac/permissions/self/ 
# /api/view/rbac/permissions/ 
 
# /api/view/rbac/roles/
# /api/view/rbac/user-roles-assign/
