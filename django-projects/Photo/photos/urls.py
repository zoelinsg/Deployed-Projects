from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'photos', views.PhotoViewSet)
router.register(r'albums', views.AlbumViewSet)

urlpatterns = [
    path('', views.AlbumListView.as_view(), name='home'),  # 設置相簿列表為首頁
    path('upload/', views.upload_photos, name='upload_photos'),  # 上傳相片
    path('photos/', views.PhotoListView.as_view(), name='photo_list'),  # 相片列表
    path('photos/<int:pk>/', views.PhotoDetailView.as_view(), name='photo_detail'),  # 相片詳情
    path('photos/<int:pk>/edit/', views.PhotoUpdateView.as_view(), name='photo_edit'),  # 編輯相片
    path('photos/<int:pk>/delete/', views.PhotoDeleteView.as_view(), name='photo_delete'),  # 刪除相片
    path('albums/<int:pk>/', views.AlbumDetailView.as_view(), name='album_detail'),  # 相簿詳情
    path('albums/add/', views.AlbumCreateView.as_view(), name='album_add'),  # 新增相簿
    path('albums/<int:pk>/edit/', views.AlbumUpdateView.as_view(), name='album_edit'),  # 編輯相簿
    path('albums/<int:pk>/delete/', views.AlbumDeleteView.as_view(), name='album_delete'),  # 刪除相簿
    path('api/', include(router.urls)),  # REST API 路由
]