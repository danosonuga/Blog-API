from django.urls import path, include
from blog_api import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = format_suffix_patterns([
    path('', views.api_overview),
    path('login/', views.LoginView.as_view(), name='login'),
    path('signup/', views.CreateUser.as_view(), name='create-user'),
    path('reset/', views.PasswordResetView.as_view(), name='reset-password'),
    path('reset/change/<uidb64>/<token>/', views.ChangePasswordView.as_view(), name='change-password'),
    path('posts/', views.PostList.as_view(), name='post-list'),
    path('posts/<int:pk>/', views.PostDetail.as_view(), name='post-detail'),
    path('posts/<int:pk>/comment/', views.PostComment.as_view(), name='comment-post'),
    path('posts/<int:pk>/like/', views.LikePostView.as_view(), name='like-post'),
    path('category/', views.CategoryList.as_view(), name='category-list'),
    path('category/<int:pk>/', views.CategoryDetail.as_view(), name='category-detail'),
])
