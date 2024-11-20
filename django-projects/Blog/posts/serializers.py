from rest_framework import serializers
from .models import Post, Tag, LikePost, BookmarkPost

# 文章序列化器
class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    tags = serializers.SlugRelatedField(slug_field='name', queryset=Tag.objects.all(), many=True)

    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'content', 'category', 'image', 'tags', 'created_at', 'updated_at', 'no_of_likes']

# 標籤序列化器
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

# 喜歡文章序列化器
class LikePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikePost
        fields = ['id', 'user', 'post']

# 收藏文章序列化器
class BookmarkPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookmarkPost
        fields = ['id', 'user', 'post']