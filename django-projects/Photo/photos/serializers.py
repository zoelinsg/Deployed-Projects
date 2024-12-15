from rest_framework import serializers
from .models import Photo, Album

# 相片序列化器
class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['id', 'title', 'description', 'image', 'author', 'album', 'category', 'location', 'tags', 'created_at', 'updated_at']

# 相簿序列化器
class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ['id', 'name', 'description', 'author', 'created_at', 'updated_at']