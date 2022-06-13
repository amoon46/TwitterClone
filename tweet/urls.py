from django.urls import path

from . import views

app_name = 'tweet'

urlpatterns = [
    path('top/', views.TopView.as_view(), name='top'),
    path('post_create/', views.CreatePostView.as_view(), name='post_create'),
    path('posts/<int:pk>/detail/', views.DetailPostView.as_view(), name='post_detail'),
    path('posts/<int:pk>/update/', views.UpdatePostView.as_view(), name='post_update'),
    path('posts/<int:pk>/delete/', views.DeletePostView.as_view(), name='post_delete'),
    path('like/<int:pk>/', views.LikeView.as_view(), name='like'),
    path('unlike/<int:pk>/', views.UnLikeView.as_view(), name='unlike'),
    path('follow/<int:pk>/', views.UserFollowView.as_view(), name='follow'),
    path('unfollow/<int:pk>/', views.UserUnFollowView.as_view(), name='unfollow'),
    path('following/<int:pk>/list/', views.UserFollowingListView.as_view(), name='following_list'),
    path('followers/<int:pk>/list/', views.UserFollowersListView.as_view(), name='followers_list'),
]
