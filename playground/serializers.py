from rest_framework import serializers


class EmailSubscribeSerializer(serializers.Serializer):
    email = serializers.EmailField()
