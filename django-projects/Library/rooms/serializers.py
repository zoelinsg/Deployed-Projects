from rest_framework import serializers
from .models import Room

# 自修室序列化器
class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'