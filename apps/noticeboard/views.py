from django.db.models import Q

from .models import Event, Notice
from .serializers import EventSerializer, NoticeSerializer
from kernel.viewsets import BaseViewSet


class EventViewSet(BaseViewSet):
    serializer_class = EventSerializer

    def get_queryset(self):
        user = self.request.user

        # Superuser can see all
        if user.is_superuser:
            return Event.objects.all()

        user_role_ids = user.user_roles.values_list("role_id", flat=True)
        return Event.objects.filter(Q(event_for__isnull=True) | Q(event_for_id__in=user_role_ids)).distinct()


class NoticeViewSet(BaseViewSet):
    serializer_class = NoticeSerializer

    def get_queryset(self):
        user = self.request.user

        # Superuser can see all
        if user.is_superuser:
            return Notice.objects.all()

        user_role_ids = user.user_roles.values_list("role_id", flat=True)
        return Notice.objects.filter(Q(notice_for__isnull=True) | Q(notice_for_id__in=user_role_ids)).distinct()
    
    