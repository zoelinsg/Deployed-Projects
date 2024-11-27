from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('category/<str:category_name>/', views.product_category, name='product_category'),
    path('search/', views.product_search, name='product_search'),
    path('api/products/', views.api_product_list, name='api_product_list'),
    path('api/products/<int:pk>/', views.api_product_detail, name='api_product_detail'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='product_list'), name='logout'),
]