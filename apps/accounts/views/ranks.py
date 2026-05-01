from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.accounts.models import Rank, User
from apps.accounts.serializers import RankSerializer, UserSerializer

class RankViewSet(ModelViewSet):
    permisisons_classes = [IsAuthenticated]
    queryset = Rank.objects.all()
    serializer_class = RankSerializer

 
class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    # /users/ - all except superusers
    def get_queryset(self):
        return User.objects.filter(is_superuser=False)

    # /users/admin/ - only superusers
    @action(detail=False, methods=["get"], url_path="admin", permission_classes=[IsAdminUser])
    def admin_users(self, request):
        admins = User.objects.filter(is_superuser=True)
        serializer = self.get_serializer(admins, many=True)
        return Response(serializer.data)
    
    # /users/self/ - only superusers
    @action(detail=False, methods=["get"], url_path="self", permission_classes=[IsAuthenticated])
    def self_users(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)