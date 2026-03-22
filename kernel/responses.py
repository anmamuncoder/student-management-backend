from rest_framework.response import Response

def BaseResponse(data=None, message="", success=True, status=200):
    return Response({
        "success": success,
        "message": message,
        "data": data
    }, status=status)


