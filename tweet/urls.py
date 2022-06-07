from django.urls import path

from . import views

app_name = 'tweet'

urlpatterns = [
    path('top/', views.TopView.as_view(), name='top'),
    path('post_create/', views.CreatePostView.as_view(), name='post_create'),
    path('posts/<int:pk>/detail/', views.DetailPost.as_view(), name='post_detail'),
    path('posts/<int:pk>/update/', views.UpdatePost.as_view(), name='post_update'),
    path('posts/<int:pk>/delete/', views.DeletePost.as_view(), name='post_delete'),
    path('like/<int:pk>/', views.Like.as_view(), name='like'),
    path('unlike/<int:pk>/', views.UnLike.as_view(), name='unlike'),
    path('follow/<int:pk>/', views.UserFollow.as_view(), name='follow'),
    path('unfollow/<int:pk>/', views.UserUnFollow.as_view(), name='unfollow'),
    path('following/<int:pk>/list/', views.UserFollowingList.as_view(), name='following_list'),
    path('followers/<int:pk>/list/', views.UserFollowersList.as_view(), name='followers_list'),
]
