from urllib import response
from rest_framework import serializers

class QuerySerializer(serializers.Serializer):
    query = serializers.CharField(max_length=500, allow_blank=False)
    response = serializers.CharField(read_only=True)