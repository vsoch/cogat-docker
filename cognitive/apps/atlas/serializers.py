from rest_framework import serializers

from .query import Task

class TaskSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
