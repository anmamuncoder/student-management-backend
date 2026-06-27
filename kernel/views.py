from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from apps.course.models import Course, Subject, Module, Syllabus, Batch

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
    
 
class UniqueCodeAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, type_name):

        if type_name == "subject":
            model = Subject

        elif type_name == "module":
            model = Module

        else:
            return Response(
                {"error": "Invalid type"},
                status=status.HTTP_400_BAD_REQUEST
            )

        code =  1000 + model.objects.count() + 1
        
        while model.objects.filter(code=code).exists():
            code = str(int(code) + 1)
            
        return Response({
            "type": type_name,
            "code": code
        })
    