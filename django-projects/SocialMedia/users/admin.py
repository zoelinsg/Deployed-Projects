from django.contrib import admin
from .models import Profile, Post, LikePost, FollowersCount

# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'profileimg', 'location')

class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'image', 'caption', 'created_at','no_of_likes')

class LikePostAdmin(admin.ModelAdmin):
    list_display = ('post_id', 'username')

class FollowersCountAdmin(admin.ModelAdmin):
    list_display = ('follower', 'user')


admin.site.register(Profile, ProfileAdmin)  #註冊至Administration(管理員後台)
admin.site.register(Post, PostAdmin)  #註冊至Administration(管理員後台)
admin.site.register(LikePost, LikePostAdmin)  #註冊至Administration(管理員後台)
admin.site.register(FollowersCount, FollowersCountAdmin)  #註冊至Administration(管理員後台)