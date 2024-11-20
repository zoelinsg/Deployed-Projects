from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='home'),  # 首頁，顯示所有文章
    path('post/<uuid:pk>/', views.post_detail, name='post_detail'),  # 文章詳情頁面
    path('search/', views.post_search, name='post_search'),  # 文章搜尋
    path('category/<str:category>/', views.post_category, name='post_category'),  # 文章分類
    path('my_posts/', views.my_posts, name='my_posts'),  # 我的文章
    path('post/create/', views.post_create, name='post_create'),  # 創建文章
    path('post/<uuid:pk>/update/', views.post_update, name='post_update'),  # 更新文章
    path('post/<uuid:pk>/delete/', views.post_delete, name='post_delete'),  # 刪除文章
    path('post/<uuid:pk>/like/', views.like_post, name='like_post'),  # 喜歡文章
    path('post/<uuid:pk>/bookmark/', views.bookmark_post, name='bookmark_post'),  # 收藏文章
    path('my_liked_posts/', views.my_liked_posts, name='my_liked_posts'),  # 我喜歡的文章
    path('my_bookmarked_posts/', views.my_bookmarked_posts, name='my_bookmarked_posts'),  # 我收藏的文章
]