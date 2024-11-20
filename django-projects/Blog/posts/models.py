from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime

User = get_user_model()

# 預設圖片路徑
DEFAULT_IMAGE_PATH = 'post_images/default.jpg'

# 固定六個類別
CATEGORY_CHOICES = [
    ('Tech', '科技'),
    ('Health', '健康'),
    ('Travel', '旅遊'),
    ('Food', '美食'),
    ('Lifestyle', '生活'),
    ('Education', '教育'),
    ('Others', '其他')
]

# 文章模型
class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_images', default=DEFAULT_IMAGE_PATH)
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)  # 使用選項來表示類別
    tags = models.ManyToManyField('Tag', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # 創建日期
    updated_at = models.DateTimeField(auto_now=True)  # 最後修改日期
    no_of_likes = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def update_likes_count(self):
        self.no_of_likes = self.likes.count()
        self.save()

# 喜歡文章模型
class LikePost(models.Model):
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='liked_posts', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} 喜歡 {self.post.title}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.post.update_likes_count()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.post.update_likes_count()

# 收藏文章模型
class BookmarkPost(models.Model):
    post = models.ForeignKey(Post, related_name='bookmarks', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='bookmarked_posts', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} 收藏 {self.post.title}'

# 標籤模型
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

# 評論模型
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author} on {self.post}"