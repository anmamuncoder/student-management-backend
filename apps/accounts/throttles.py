from rest_framework.throttling import UserRateThrottle
import time
from django.core.cache import cache
from rest_framework.throttling import BaseThrottle

# ------------------------------------------
# Basic throllel and also use in setting  |  'forgot_password': '1/minute',
# ------------------------------------------
# class ForgotPasswordThrottle(UserRateThrottle):
#     scope = 'forgot_password'


# ------------------------------------------
# Custom throttle to allow only one forgot-password request per IP every 5 minutes
# Ensure caching is configured (e.g., LocMemCache for dev or Redis for production) so the throttle works reliably.
# ------------------------------------------
class ForgotPasswordThrottle(BaseThrottle):
    def allow_request(self, request, view):
        self.key = f"forgot_{request.META.get('REMOTE_ADDR')}"
        
        self.last_request = cache.get(self.key)

        if self.last_request:
            self.remaining = 300 - (time.time() - self.last_request)
            if self.remaining > 0:
                return False
                # For custom throttled message
                # raise Throttled(detail=f"Please wait {int(remaining // 60)} minutes {int(remaining % 60)} seconds before retrying.")

        cache.set(self.key, time.time(), timeout=300)
        return True

    def wait(self):
        return max(0, int(self.remaining)) if hasattr(self, 'remaining') else None

