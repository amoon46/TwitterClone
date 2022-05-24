from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('twitter.urls')),
    path('user/', include('user.urls')),
    path('tweet/', include('tweet.urls')),
]

"""
やること：test機能の実装

分からなかったこと：listview, detailviewの違い
"""
