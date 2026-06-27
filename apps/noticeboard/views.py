from django.db.models import Q

from .models import Event, Notice
from .serializers import EventSerializer, NoticeSerializer
from kernel.viewsets import BaseViewSet
from rest_framework.permissions import IsAuthenticated


class EventViewSet(BaseViewSet):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # Superuser can see all
        if user.is_superuser:
            return Event.objects.all().order_by('-created_at')

        user_role_ids = user.user_roles.values_list("role_id", flat=True)
        return Event.objects.filter(Q(event_for__isnull=True) | Q(event_for_id__in=user_role_ids)).distinct().order_by('-created_at')


class NoticeViewSet(BaseViewSet):
    serializer_class = NoticeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # Superuser can see all
        if user.is_superuser:
            return Notice.objects.all().order_by('-created_at')

        user_role_ids = user.user_roles.values_list("role_id", flat=True)
        return Notice.objects.filter(Q(notice_for__isnull=True) | Q(notice_for_id__in=user_role_ids)).distinct().order_by('-created_at')
    
    