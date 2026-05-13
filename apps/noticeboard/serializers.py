from rest_framework.serializers import ModelSerializer
from .models import Event, Notice


class EventSerializer(ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"


class NoticeSerializer(ModelSerializer):
    class Meta:
        model = Notice
        fields = "__all__"