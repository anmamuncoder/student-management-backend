from rest_framework.views import APIView
from rest_framework.response import Response

#--------------------------------
# BaseAPIView to standardize API responses for all APIViews
#--------------------------------

class BaseAPIView(APIView):

    def success_response(self, data=None, message="", status_code=200):
        return Response({
            "success": True,
            "message": message,
            "data": data
        }, status=status_code)

    def error_response(self, errors=None, message="Request failed", status_code=400):
        return Response({
            "success": False,
            "message": message,
            "errors": errors
        }, status=status_code)
    
