from rest_framework import serializers
from .models import Record

class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record  # 指定模型
        fields = '__all__'  # 序列化所有欄位