from django.contrib.auth.models import User, Group
from .views import Song
from rest_framework import serializers


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        #which means all fields
        fields = [field.name for field in Song._meta.get_fields()]


