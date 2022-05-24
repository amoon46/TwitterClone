from django.urls import path

from . import views

app_name = 'tweet'

urlpatterns = [
    path('top/', views.TopView.as_view(), name='top'),
    path('mypost/', views.MyPostView.as_view(), name='mypost'),
    path('post_create/', views.CreatePostView.as_view(), name='post_create'),
    path('posts/<int:pk>/detail/', views.DetailPost.as_view(), name='post_detail'),
    path('posts/<int:pk>/update/', views.UpdatePost.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', views.DeletePost.as_view(), name='post_delete'),
    path('like/<int:pk>/home/', views.LikeHome.as_view(), name='like_home'),
    path('like/<int:pk>/detail/', views.LikeProfile.as_view(), name='like_profile'),
    path('like/<int:pk>/list/', views.LikeList.as_view(), name='like_list'),
    path('follow/<int:pk>/', views.UserFollow.as_view(), name='follow'),
    path('followees/<int:pk>/list/', views.UserFolloweesList.as_view(), name='followees_list'),
    path('followers/<int:pk>/list/', views.UserFollowersList.as_view(), name='followers_list'),
]
