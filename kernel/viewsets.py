from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

#--------------------------------
# BaseModelViewSet to standardize API responses for all ModelViewSets
#--------------------------------
class BaseModelViewSet(ModelViewSet):

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)

        return Response({
            "success": True,
            "message": "Data fetched",
            "data": response.data
        })

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)

        return Response({
            "success": True,
            "message": "Data retrieved",
            "data": response.data
        })

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        return Response({
            "success": True,
            "message": "Created successfully",
            "data": response.data
        })

