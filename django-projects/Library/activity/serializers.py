from rest_framework import serializers
from .models import Activity

# 活動序列化器
class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = '__all__'