import re
import logging
from django.http import JsonResponse

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

from apps.rbac.utils import _is_exempt, _get_resource_from_path, get_user_permissions
from apps.rbac.config import HTTP_METHOD_ACTION_MAP


logger = logging.getLogger(__name__)


class RBACMiddleware:
    """
    Middleware-based Role-Based Access Control.

    Flow:
        1. Exempt path? -> pass through
        2. JWT authenticate -> 401 if failed
        3. Superuser? -> pass through
        4. Map URL -> resource, HTTP method -> action
        5. Build permission slug: "resource:action"
        6. Check slug in user's permissions -> 403 if not found
        7. Pass through to view
    """

    def __init__(self, get_response): 

        self.get_response = get_response
        self._authenticator = JWTAuthentication()

    def __call__(self, request, *args, **kwds): 

        path = request.path
        method = request.method
 
        # -------------------------------
        # Step 1: Skip Exempt paths 
        # -------------------------------
        if _is_exempt(path): 
            return self.get_response(request)

        # Check only /api/ routes handle 
        if not path.startswith('/api/'): 
            return self.get_response(request)

        # OPTIONS always allow (CORS preflight)
        if method == 'OPTIONS': 
            return self.get_response(request)

        # -------------------------------
        # Step 2: User authenticated check form JWT  
        # -------------------------------
        user = self._get_authenticated_user(request)
        if user is None: 
            return self._error('Authentication credentials were not provided or are invalid.',401)

        # ------------------------------- 
        # Step 3: Superuser bypass
        # -------------------------------
        if user.is_superuser: 
            request.user = user
            return self.get_response(request)

        # ------------------------------- 
        # Step 4: Find URL to resource, HTTP to action
        # -------------------------------
        resource = _get_resource_from_path(path) 

        if resource is None:
            request.user = user
            return self.get_response(request)
 
        action = HTTP_METHOD_ACTION_MAP.get(method) 

        if action is None: 
            request.user = user
            return self.get_response(request)

        # -------------------------------
        # Step 5: Permission slug build koro
        # -------------------------------
        required_perm = f"{resource}:{action}" 

        # -------------------------------
        # Step 6: Permission check
        # -------------------------------
        user_perms = get_user_permissions(user) 

        if required_perm not in user_perms:
            logger.warning(
                "Permission denied | user=%s | required=%s | path=%s | method=%s",
                user.id, required_perm, path, method
            )

            return self._error(f"You do not have permission to perform this action.",403,
                extra=
                {
                    'required_permission': required_perm,
                    'your_permissions': sorted(user_perms),
                }
            )
        
        # Step 7: All good
        request.user = user 

        return self.get_response(request)

    def _get_authenticated_user(self, request):
        """JWT token validate kore user return koro, fail hole None."""
        try:
            result = self._authenticator.authenticate(request)
            if result:
                user, token = result
                return user
        except (InvalidToken, TokenError) as e:
            logger.debug("JWT auth failed: %s", str(e))
        return None

    @staticmethod
    def _error(message: str, status: int, extra: dict = None):
        body = {
            "status": False,
            "errors": {
                "message": message
            }
        }
        if extra:
            body["errors"].update(extra)
            
        return JsonResponse(body, status=status)

        