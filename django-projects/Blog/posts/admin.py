from django.contrib import admin
from .models import Post, LikePost, BookmarkPost, Tag

# 註冊文章模型到管理後台
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'created_at', 'updated_at', 'no_of_likes')
    search_fields = ('title', 'content')
    list_filter = ('category', 'created_at', 'updated_at')
    ordering = ('-created_at',)

# 註冊喜歡文章模型到管理後台
@admin.register(LikePost)
class LikePostAdmin(admin.ModelAdmin):
    list_display = ('user', 'post')
    search_fields = ('user__username', 'post__title')

# 註冊收藏文章模型到管理後台
@admin.register(BookmarkPost)
class BookmarkPostAdmin(admin.ModelAdmin):
    list_display = ('user', 'post')
    search_fields = ('user__username', 'post__title')

# 註冊標籤模型到管理後台
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)